from django.http import FileResponse, Http404, HttpResponse, JsonResponse
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound
from django.core.exceptions import ObjectDoesNotExist


# from .serializers import SubjectSerializer, ChapterSerializer, QuestionSerializer, AnswerSmcqSerializer, AnswerMmcqSerializer, AnswerIntegerTypeSerializer
from .models import Test, LiveTest, TestAttempt, TestQuestion, TestQuestionAttempt
from questions.models import Question, AnswerIntegerType, AnswerMmcq, AnswerSmcq

# from django.core import serializers

# Create your views here.

# test list

class TestList(APIView):
  
  permission_classes = [IsAuthenticated]
  
  def get(self, request, format=None):
    user = request.user
    queryset = Test.objects.filter(user_id = user.id)
    return HttpResponse({'message' : f'hello {user.name} !'})


# admin side - post - create new mock test by ui
# admin side - post - create new LIVE mock test by ui

# start mock test - post - create attempt object
    # if mock test is LIVE - check start_time
class StartTest(APIView):
  def post(self, request, format=None):
    test_id = self.request.POST.get_query_params("test_id")
    # user_id = self.request.POST.get_query_params("user_id")
    user = request.user
    print(test_id, user)

    return Response(status=status.HTTP_200_OK)

# submit mock test - put - test attempt end time update