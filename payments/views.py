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

from accounts.models import User  
from .models import Order

# CASHFREE CONFIG

Cashfree.XClientId = config('XClientId')
Cashfree.XClientSecret = config('XClientSecret')

if settings.DEBUG:
  Cashfree.XEnvironment = Cashfree.XSandbox
else:
  Cashfree.XEnvironment = Cashfree.XProduction

x_api_version = "2023-08-01"

# VIEWS

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

    customerDetails = CustomerDetails(customer_id=f"USER{user.id}", customer_phone=f"{mobile_no}", customer_email=user.email)
    orderMeta = OrderMeta(return_url=request.data['return_url'])
    createOrderRequest = CreateOrderRequest(order_amount=request.data['amount'], order_currency="INR", customer_details=customerDetails, order_meta=orderMeta)
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

    try:
      user_id = data['data']['customer_details']['customer_id'][4:]
      user = User.objects.get(id=user_id)
    except Exception as e:
      print("Error while finding user : ", e)
      return Response({'success':False,'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    
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
    
    try:
      if data['data']['payment']['payment_status'] == 'SUCCESS':
        user.is_payment_done=True
        user.save()
    except Exception as e:
      print(e)
      return Response({'success':False,'message': 'User not updated'}, status=status.HTTP_400_BAD_REQUEST)

    return Response({'success':True,'message': 'Webhook Received'}, status=status.HTTP_200_OK)
