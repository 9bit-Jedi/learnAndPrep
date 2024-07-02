from django.core.mail import EmailMessage
import os, requests
from django.conf import settings

import phonenumbers
from phonenumbers.phonenumberutil import NumberParseException

import random
from datetime import datetime, timedelta
from django.utils import timezone


def normalize_phone_number(phone_number, default_country_code="IN"):
    # parsed_number = phonenumbers.parse(phone_number, default_country_code)

    try:
        # Try parsing without explicit region first
        parsed_number = phonenumbers.parse(phone_number)
    except NumberParseException as e:
        if e.error_type == NumberParseException.INVALID_COUNTRY_CODE:
            # If no region is found, try with default_country_code
            try:
                parsed_number = phonenumbers.parse(phone_number, default_country_code)
            except NumberParseException as e:
                print("Invalid phone number: Missing or invalid country code", e )
                return None
        else:
            # Other parsing errors
            print(f"Invalid phone number: {e}")
            return None
    ##
    
    print(parsed_number)
    if phonenumbers.is_valid_number(parsed_number):
        # Format without '+' and remove leading zeros
        return phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.E164)[1:].lstrip("0")
    else:
        print ("Invalid phone number")
    # try:
    # except phonenumbers.phonenumberutil.NumberParseException:
    #     pass
 

class Util:
    @staticmethod
    def generate_otp():
        otp = str(random.randint(100000, 999999))
        otp_created_at = timezone.now().isoformat()   # Record the OTP creation time
        return otp, otp_created_at
    
    @staticmethod
    def is_otp_expired(otp_created_at):
        expiry_duration = timedelta(minutes=10)  # Define OTP expiration duration (e.g., 5 minutes)
        now = timezone.now()
        return (now - datetime.fromisoformat(otp_created_at)) > expiry_duration

    @staticmethod
    def send_mail(data):
        email = EmailMessage(
            subject=data['subject'],
            body= data['body'],
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[data['to_email']],
       
        )
        email.send()

    # def generate_otp():
    #     return str(random.randint(100000, 999999))
    
    @staticmethod
    def send_whatsapp_otp(otp, mobile_no):
        """
        Send OTP via Whatsapp.
        """
        # mobile_no = "9315117745" 
        mobile_no = normalize_phone_number(mobile_no)
        print(type(mobile_no), mobile_no) 

        url = f"https://graph.facebook.com/v19.0/{settings.PHONE_NUMBER_ID}/messages"
        headers = {'content-type': 'application/json', "Authorization": f"Bearer {settings.WHATSAPP_AUTH_TOKEN}"}
        payload = {"messaging_product": "whatsapp", "to": mobile_no, "type": "template", "template": {"name": "otp", "language": {"code": "en"}, "components": [{"type": "body", "parameters": [{"type": "text", "text": otp}]}, {"type": "button", "sub_type": "Url", "index": 0, "parameters": [{"type": "payload", "payload": otp}]}]}}

        response = requests.post(url, json=payload, headers=headers)
        print(response.content)
        return response
        
