from django.contrib import admin
from .models import Order, Coupon

# Register your models here.
admin.site.register(Order)
admin.site.register(Coupon)