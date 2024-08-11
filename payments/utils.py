from django.core.mail import EmailMessage
import os, requests
from django.conf import settings

from django.core.mail import send_mail, EmailMessage
from .email_backends import PaymentsEmailBackend


class Util:
    @staticmethod
    def send_payments_mail(data):

        mail = EmailMessage(
            data['subject'],
            data['body'],
            settings.EMAIL_HOST_USER,
            [data['to_email']]
        )
        mail.connection = PaymentsEmailBackend()
        mail.send()
