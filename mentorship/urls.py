from django.urls import path
from .views import *
urlpatterns = [
    path('predict', predictCompatibility.as_view(), name='predict'),
]