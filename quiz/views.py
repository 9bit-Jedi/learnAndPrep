from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status

from .models import Quiz, QuizQuestion
from .serializers import QuizSerializer

# Create your views here.
class GetQuiz(APIView):
  def get(self, request, format=None):
    queryset = Quiz.objects.all()
    serializer = QuizSerializer(queryset, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)