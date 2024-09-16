from django.conf import settings
from django.shortcuts import render
from decouple import config

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status

from cashfree_pg.models.create_order_request import CreateOrderRequest
from cashfree_pg.models.order_meta import OrderMeta
from cashfree_pg.api_client import Cashfree
from cashfree_pg.models.customer_details import CustomerDetails
import phonenumbers

from django.template.loader import render_to_string
from django.utils.html import strip_tags

from accounts.models import User
from .utils import Util
from .models import Order, Coupon
from .serializers import CouponSerializer

# CASHFREE CONFIG

Cashfree.XClientId = config('XClientId')
Cashfree.XClientSecret = config('XClientSecret')

if settings.DEBUG:
  Cashfree.XEnvironment = Cashfree.XSandbox
else:
  Cashfree.XEnvironment = Cashfree.XProduction

x_api_version = "2023-08-01"

# VIEWS

class ApplyCouponView(APIView):
  def get(self, request):
    # coupon_code = request.data['coupon_code']
    coupon_code = request.data.get('coupon_code', None)
    try:
      coupon_code = Coupon.objects.get(code=coupon_code)
      serializer = CouponSerializer(coupon_code)
      if coupon_code.is_valid():
        amount = request.data.get('amount', 5000)
        # amount = 4999
        amount = int(amount*(100 - coupon_code.discount)/100)
        return Response({'success':True, 'message': 'Coupon is valid', 'coupon_details': serializer.data, 'order_total':amount}, status=status.HTTP_200_OK)
      else:
        return Response({'success':False, 'message': 'Coupon is invalid or expired'}, status=status.HTTP_400_BAD_REQUEST)
    except Coupon.DoesNotExist as e:  
      print("Error while finding coupon : " , e)
      return Response({'success':False, 'message': 'Coupon not found'}, status=status.HTTP_404_NOT_FOUND)

class CreateOrderView(APIView):
  def post(self, request):
    try:
      user = request.user
      user = User.objects.get(id=user.id)
    except Exception as e:
      print(e)
      return Response({'success':False,'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    
    #  Assuming user.phone_no is in the format "+[country_code][phone_number]"
    parsed_phone = phonenumbers.parse(user.mobile_no, None)
    mobile_no = parsed_phone.national_number

    # decide order amout based on coupon code

    amount = 4999 
    # amount = request.data.get('amount', 5000)
    
    if request.data['coupon_code']:
      coupon_code = request.data['coupon_code']
      # coupon_code = request.data.get('coupon_code', None)
      try:
        coupon_code = Coupon.objects.get(code=coupon_code)
        if coupon_code.is_valid():
          amount = int(amount*(100 - coupon_code.discount)/100)
        else:
          return Response({'success':False,'message': 'Coupon is invalid or expired'}, status=status.HTTP_400_BAD_REQUEST)
      except Coupon.DoesNotExist as e:  
        print("Error while finding coupon : " , e)
        return Response({'success':False,'message': 'Coupon not found'}, status=status.HTTP_404_NOT_FOUND)

    customerDetails = CustomerDetails(customer_id=f"USER{user.id}", customer_phone=f"{mobile_no}", customer_email=user.email)
    orderMeta = OrderMeta(return_url=request.data['return_url'], notify_url=f'{settings.BASE_URL}/api/payments/webhook/')
    createOrderRequest = CreateOrderRequest(order_amount=amount, order_currency="INR", customer_details=customerDetails, order_meta=orderMeta)
    print('webhook url : ', f'{settings.BASE_URL}/api/payments/webhook/')
    print("amount : ", amount)
    try:
      api_response = Cashfree().PGCreateOrder(x_api_version, createOrderRequest, None, None) 
    except Exception as e:
      print(e)
      return Response({'success':False,'message': 'Order Creation Failed'}, status=status.HTTP_400_BAD_REQUEST)

    return Response({ 'success':True,
                      'message': 'Order Created', 
                      'session_id': api_response.data.payment_session_id, 
                      "cf_order_id":api_response.data.cf_order_id, 
                      "order_id":api_response.data.order_id,}, status=status.HTTP_200_OK)

class PaymentWebhookView(APIView):
  def post(self, request):
    print('webhook received')
    data = request.data
    print(data)

    try:
      user_id = data['data']['customer_details']['customer_id'][4:]
      user = User.objects.get(id=user_id)
    except Exception as e:
      print("Error while finding user : ", e)
      return Response({'success':False,'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    # Create Order object in db
    
    try:
      order = Order.objects.create(
        user_details=user,
        cf_order_id=data['data']['payment']['cf_payment_id'], 
        order_id=data['data']['order']['order_id'], 
        order_currency=data['data']['payment']['payment_currency'], 
        order_amount=data['data']['payment']['payment_amount'], 
        order_status=data['data']['payment']['payment_status']
      )
      order.save()
    except Exception as e:  
      print("Error while creating Order object in db : " , e)
      return Response({'success':False, 'message': f"Order not saved. Error : {e}"}, status=status.HTTP_400_BAD_REQUEST)
    
    # Send Payment webhook to the user's email

    context = {
      'user': user,
      'order': order,
      'payment': data['data']['payment']
    }
    
    if data['data']['payment']['payment_status'] == 'SUCCESS':
      html_message = render_to_string("success_email.html", context=context)
      email_data = {
      'subject': 'Payment Successful - VJ Nucleus Mentorship',
      'body': strip_tags(html_message),
      'to_email': user.email,
      'template_name': 'success_email.html', 
    }
    else:
      html_message = render_to_string("failure_email.html", context=context)
      email_data = {
      'subject': 'Payment Unsuccessful - VJ Nucleus Mentorship',
      'body': strip_tags(html_message),
      'to_email': user.email,
      'template_name': 'failure_email.html', 
    }

    Util.send_payments_mail(email_data, context)
    
    #  send message on whatsapp for confirmation    # later (sent message template request on whatsapp)

    # Update user payment status (in User model)

    try:
      if data['data']['payment']['payment_status'] == 'SUCCESS':
        user.is_payment_done=True
        user.save()
        print('User payment status updated')
    except Exception as e:
      print(e)
      return Response({'success':False,'message': 'User not updated'}, status=status.HTTP_400_BAD_REQUEST)

    return Response({'success':True,'message': 'Webhook Received'}, status=status.HTTP_200_OK)
