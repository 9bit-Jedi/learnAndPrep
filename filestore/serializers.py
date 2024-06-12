from rest_framework import serializers
from .models import Files

class Fileserializer(serializers.ModelSerializer):
    class Meta:
        model = Files
        fields = ['id' , 'pdf' , 'title']