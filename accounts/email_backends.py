from django.core.mail.backends.smtp import EmailBackend
from django.conf import settings

class OtpEmailBackend(EmailBackend):
    def __init__(self, *args, **kwargs):
        kwargs['username'] = settings.OTP_EMAIL_HOST_USER
        kwargs['password'] = settings.OTP_EMAIL_HOST_PASSWORD
        super().__init__(*args, **kwargs)

class SupportEmailBackend(EmailBackend):
    def __init__(self, *args, **kwargs):
        kwargs['username'] = settings.SUPPORT_EMAIL_HOST_USER
        kwargs['password'] = settings.SUPPORT_EMAIL_HOST_PASSWORD
        super().__init__(*args, **kwargs)