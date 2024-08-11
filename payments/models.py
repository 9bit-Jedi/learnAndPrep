from django.db import models
from django.utils import timezone

from accounts.models import User
# Create your models here.
class Order(models.Model):
    user_details = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    cf_order_id = models.CharField(max_length=255)
    order_id = models.CharField(max_length=255)
    order_currency = models.CharField(max_length=10)
    # order_amount = models.DecimalField(max_digits=10, decimal_places=2)
    order_amount = models.IntegerField()
    order_status = models.CharField(max_length=50)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user_details.name}_{self.order_status}_{self.order_id}"