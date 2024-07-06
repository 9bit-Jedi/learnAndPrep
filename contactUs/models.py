from django.db import models

# Create your models here.

class ContactUs(models.Model):
    sno = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64)
    email = models.EmailField()
    mobile_no = models.CharField(max_length=15)
    subject = models.CharField(max_length=172)
    message = models.TextField(max_length=1024)
    timestamp = models.DateTimeField(auto_now_add=True , blank=True)
    
    def __str__(self):
        return f"{self.name} - {self.subject}"