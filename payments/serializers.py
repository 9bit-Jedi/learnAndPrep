from rest_framework import serializers
from .models import Order, Coupon

class CouponSerializer(serializers.ModelSerializer):
  class Meta:
    model = Coupon
    fields = '__all__'