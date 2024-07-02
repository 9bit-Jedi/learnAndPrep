from .models import ContactUs
from rest_framework import serializers

class ContactUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactUs
        fields = ['name', 'email', 'mobile_no', 'subject', 'message']