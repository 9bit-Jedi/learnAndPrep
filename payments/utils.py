from django.core.mail import EmailMessage
import os, requests
from django.conf import settings

from django.core.mail import send_mail, EmailMessage, EmailMultiAlternatives
from .email_backends import PaymentsEmailBackend

from django.template.loader import render_to_string

class Util:
    @staticmethod
    def send_payments_mail(data, context):

        html_message = render_to_string(data["template_name"], context=context)

        mail = EmailMultiAlternatives(
            subject = data['subject'],
            body = data['body'],
            from_email = settings.PAYMENTS_EMAIL_HOST_USER,
            to = [data['to_email']]
        )
        mail.attach_alternative(html_message, "text/html")
        mail.connection = PaymentsEmailBackend()
        mail.send()
    # @staticmethod
    # def send_payments_mail(data):

    #     mail = EmailMessage(
    #         data['subject'],
    #         data['body'],
    #         settings.EMAIL_HOST_USER,
    #         [data['to_email']]
    #     )
    #     mail.connection = PaymentsEmailBackend()
    #     mail.send()
