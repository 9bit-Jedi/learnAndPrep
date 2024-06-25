from django.core.mail import EmailMessage
import os
from django.conf import settings
import random
from datetime import datetime, timedelta

class Util:
    @staticmethod
    def generate_otp():
        otp = str(random.randint(100000, 999999))
        otp_created_at = datetime.now().isoformat()   # Record the OTP creation time
        return otp, otp_created_at
    
    @staticmethod
    def is_otp_expired(otp_created_at):
        expiry_duration = timedelta(minutes=30)  # Define OTP expiration duration (e.g., 5 minutes)
        now = datetime.now()
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
    
    # @staticmethod
    # def send_sms(mobile_no, message):
    #     client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    #     client.messages.create(
    #         body=message,
    #         from_=settings.TWILIO_PHONE_NUMBER,
    #         to=mobile_no
    #     )
        
