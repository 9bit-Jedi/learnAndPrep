from rest_framework import serializers
from .models import File
  
class FileSerializer(serializers.ModelSerializer):
  class Meta :
    model = File
    fields = ("file", 'uploaded_at')
  
  # def to_representation(self, instance):
  #   representation = super().to_representation(instance)
  #   file = {
  #     "url": representation.pop("file"),
  #     "size": instance.file.size,
  #     "name": instance.file.name,
  #   }
  #   representation['file'] = file
  #   return representation