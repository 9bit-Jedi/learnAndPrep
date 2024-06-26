from django import views
from django.http import HttpResponse, FileResponse
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from django.core.files.images import ImageFile
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Notes
from .serializers import NotesSerializer

# Create your views here.

class ListNotes(APIView):
  def get(self, request, subject_id, format=None):
    
    # notes = get_object_or_404(Notes, chapter__subject_id__id=subject_id)
    try:
      notes = Notes.objects.filter(chapter__subject_id__id=subject_id)
    except ObjectDoesNotExist as e:
      return Response({"error":e}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = NotesSerializer(notes, many=True)
    return Response(serializer.data)


class GetNotes(APIView):
  def get(self, request, pdf_url, format=None):    
    
    full_path = f'media/notes/{pdf_url}'
    return FileResponse(open(full_path, 'rb'))