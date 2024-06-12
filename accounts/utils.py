from django.core.mail import EmailMessage
import os
from django.conf import settings

class Util:
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
        
