from django.conf import settings
from django.test import TestCase
from decouple import config


from cashfree_pg.models.create_order_request import CreateOrderRequest
from cashfree_pg.api_client import Cashfree
from cashfree_pg.models.customer_details import CustomerDetails


# Create your tests here.

Cashfree.XClientId = config('XClientId')
Cashfree.XClientSecret = config('XClientSecret')

Cashfree.XEnvironment = Cashfree.XSandbox
# Cashfree.XEnvironment = Cashfree.XProduction

x_api_version = "2023-08-01"

# VIEWS
def create_order():
    customerDetails = CustomerDetails(customer_id='userid', customer_phone='9315117745')
    createOrderRequest = CreateOrderRequest(order_amount=1, order_currency="INR", customer_details=customerDetails)

    try:
        api_response = Cashfree().PGCreateOrder(x_api_version, createOrderRequest, None, None)
        print(api_response.data)
    except Exception as e:
        print(e)

if __name__ == '__main__':
    create_order()  # Create Order