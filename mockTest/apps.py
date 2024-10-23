from django.apps import AppConfig


class MockTestConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mockTest'
