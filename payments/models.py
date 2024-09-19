from django.db import models
from django.utils import timezone

from accounts.models import User
# Create your models here.

    
class Coupon(models.Model):
    code = models.CharField(max_length=255, unique=True)
    discount = models.IntegerField()   ## discount in percentage

    expiry_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    def is_valid(self):
        # Check if coupon is active and hasn't expired
        return self.is_active and self.expiry_date > timezone.now()

    def __str__(self):
        return f"{self.is_active}_{self.code}_{self.discount}"
    
class Order(models.Model):
    user_details = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    cf_order_id = models.CharField(max_length=255)
    order_id = models.CharField(max_length=255)
    order_currency = models.CharField(max_length=10)
    # order_amount = models.DecimalField(max_digits=10, decimal_places=2)
    order_amount = models.IntegerField()
    order_status = models.CharField(max_length=50)
    created_at = models.DateTimeField(default=timezone.now)

    # coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True, blank=True)  # Link to Coupon

    def __str__(self):
        return f"{self.user_details.name}_{self.order_status}_{self.order_id}"