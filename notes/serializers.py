from rest_framework import serializers
from .models import Notes  
  
class NotesSerializer(serializers.ModelSerializer):

  pdf_url = serializers.SerializerMethodField()
  class Meta:
    model = Notes
    fields = ['id','title', 'pdf_url', 'chapter']
    
  def get_pdf_url(self, obj):
    return obj.file.url if obj.file else None