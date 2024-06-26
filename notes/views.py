from django import views
from django.http import HttpResponse, FileResponse
from django.db import IntegrityError
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.files.images import ImageFile

from .models import Notes
from .serializers import NotesSerializer

# Create your views here.

class ListNotes(APIView):
  def get(self, request, chapter_id, format=None):
    
    notes = Notes.objects.filter(chapter__id=chapter_id)
    serializer = NotesSerializer(notes, many=True)
    return Response(serializer.data)


class GetNotes(APIView):
  def get(self, request, pdf_url, format=None):    
    
    full_path = f'media/notes/{pdf_url}'
    return FileResponse(open(full_path, 'rb'))