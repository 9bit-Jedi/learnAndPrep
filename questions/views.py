from django.http import Http404, HttpResponse
from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import SmcqSerializer, SubjectSerializer, ChapterSerializer, TopicSerializer
from .models import Smcq, Subject, Chapter, Topic

from django.core import serializers

# Create your views here.
  
class FetchQuestionsAll(APIView):
  
  def get(self, request, format=None):
    questions = Smcq.objects.all()
    serializer = SmcqSerializer(questions, context={"request": request}, many=True)
    print(serializer.data)
    return Response(serializer.data, status=status.HTTP_200_OK)
  
  def delete(self, request, format=None):
    questions = Smcq.objects.all()
    questions.delete()
    return Response(status=status.HTTP_200_OK)
  
class FetchQuestion(APIView):
  
  def get_object(self, id):
    try:
        return Smcq.objects.get(id=id)
    except Smcq.DoesNotExist:
        raise Http404

  def get(self, request, ques_id, format=None):
    question = self.get_object(id)
    serializer = SmcqSerializer(question)
    return Response(serializer.data)
  
class FetchSubjects(APIView):
  def get(self, request, format=None):
    subjects = Subject.objects.all()
    serializer = SubjectSerializer(subjects, many=True)
    return HttpResponse(serializer.data, status=status.HTTP_200_OK)

class FetchChapters(APIView):
  def get(self, request, format=None):
    chapters = Chapter.objects.all()
    serializer = ChapterSerializer(chapters, many=True)
    return HttpResponse(serializer.data, status=status.HTTP_200_OK)

class FetchTopics(APIView):
  def get(self, request, format=None):
    topics = Topic.objects.all()
    serializer = TopicSerializer(topics, many=True)
    return HttpResponse(serializer.data, status=status.HTTP_200_OK)