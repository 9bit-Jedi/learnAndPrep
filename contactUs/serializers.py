from .models import contactus
from rest_framework import serializers

class ContactUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = contactus
        fields = ['name', 'email', 'mobile_no', 'subject', 'message']