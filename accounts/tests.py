# from django.test import TestCase
from accounts.utils import Util
# Create your tests here.

def main():
  Util.send_whatsapp_otp("919315117745")

main()