from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import QuestionSerializer
from .models import Smcq


# Create your views here.

class FetchQuestionsAll(APIView):
  
  def get(self, request, format=None):
    questions = Smcq.objects.all()
    serializer = QuestionSerializer(questions, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
  
  def delete(self, request, form=None):
    questions = Smcq.objects.all()
    questions.delete()
    return Response(status=status.HTTP_200_OK)
    
