from django.core.mail.backends.smtp import EmailBackend
from django.conf import settings

class PaymentsEmailBackend(EmailBackend):
    def __init__(self, *args, **kwargs):
        kwargs['username'] = settings.PAYMENTS_EMAIL_HOST_USER
        kwargs['password'] = settings.PAYMENTS_EMAIL_HOST_PASSWORD
        super().__init__(*args, **kwargs)