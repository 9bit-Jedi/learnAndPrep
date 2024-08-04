from django.conf import settings
from django.shortcuts import render
from decouple import config

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status

from cashfree_pg.models.create_order_request import CreateOrderRequest
from cashfree_pg.api_client import Cashfree
from cashfree_pg.models.customer_details import CustomerDetails
import phonenumbers

from accounts.models import User  

# CASHFREE CONFIG

Cashfree.XClientId = config('XClientId')
Cashfree.XClientSecret = config('XClientSecret')

Cashfree.XEnvironment = Cashfree.XSandbox
# Cashfree.XEnvironment = Cashfree.XProduction

x_api_version = "2023-08-01"

# VIEWS

class CreateOrderView(APIView):
  def post(self, request):
    try:
      user = request.user
      user = User.objects.get(id=user.id)
      print(user)
    except Exception as e:
      print(e)
      return Response({'success':False,'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    
    #  Assuming user.phone_no is in the format "+[country_code][phone_number]"
    parsed_phone = phonenumbers.parse(user.mobile_no, None)
    mobile_no = parsed_phone.national_number

    customerDetails = CustomerDetails(customer_id=f"USER{user.id}", customer_phone=f"{mobile_no}", customer_email=user.email)
    # customerDetails = CustomerDetails(customer_id=f"USER{user.id}", customer_phone=f"{user.phone_no}", customer_email=user.email)
    createOrderRequest = CreateOrderRequest(order_amount=request.data['amount'], order_currency="INR", customer_details=customerDetails)
    
    try:
      api_response = Cashfree().PGCreateOrder(x_api_version, createOrderRequest, None, None)
      print(api_response.data)
    except Exception as e:
      print(e)
      return Response({'success':False,'message': 'Order Creation Failed'}, status=status.HTTP_400_BAD_REQUEST)
    return Response({'success':True,'message': 'Order Created', 'session_id': api_response.data.payment_session_id}, status=status.HTTP_200_OK)