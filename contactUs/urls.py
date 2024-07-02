# accounts/urls.py
from django.urls import path
from .views import ContactusView

urlpatterns = [
    # Other URL patterns
    path('send/', ContactusView.as_view(), name='contact-us'),
]
