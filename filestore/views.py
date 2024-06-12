from django.shortcuts import render
from .models import Files
from rest_framework import viewsets
from .serializers import Fileserializer
# Create your views here.
class FileViewSets(viewsets.ModelViewSet):
    queryset = Files.objects.all()
    serializer_class = Fileserializer
    
