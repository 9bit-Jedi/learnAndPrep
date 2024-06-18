from django.http import FileResponse, Http404, HttpResponse, JsonResponse
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from django.core.exceptions import ObjectDoesNotExist


from .serializers import SubjectSerializer, ChapterSerializer, QuestionSerializer, AnswerSmcqSerializer, AnswerMmcqSerializer, AnswerIntegerTypeSerializer
from .models import Subject, Chapter, AnswerSmcq, AnswerMmcq, AnswerIntegerType, Question

from django.core import serializers

# Create your views here.
  
class GetQuestionAll(APIView):
  def get(self, request, format=None):
    queryset = Question.objects.all()
    serializer = QuestionSerializer(queryset, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
  
class GetQuestionAllSrc(APIView):
  def get(self, request, src, format=None):
    queryset = Question.objects.filter(source = src.upper())
    serializer = QuestionSerializer(queryset, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

class GetQuestionSrcChapter(APIView):
  def get(self, request, src, chapter_id, format=None):
    queryset = Question.objects.filter(source = src.upper()).filter(chapter_id=chapter_id.upper())
    serializer = QuestionSerializer(queryset, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
  
class GetQuestion(APIView):
  def get(self, request, question_id, format=None):
    # question_id = request.GET.get('question_id')
    queryset = get_object_or_404(Question, pk=question_id.upper())
    # queryset = Question.objects.all()
    serializer = QuestionSerializer(queryset)
    return Response(serializer.data, status=status.HTTP_200_OK)

class ChapterList_Subject(APIView):
  def get(self, request, subject_id, format=None):
    chapters = Chapter.objects.filter(subject_id=subject_id.upper())    ## only chapters with taht subject id
    serializer = ChapterSerializer(chapters, many=True)  # Pass request to serializer

    # icon_url = 
    # data = serializer.data
    # data.append({"icon":icon_url})
    return Response(serializer.data, status=status.HTTP_200_OK)

# def GetSmcq(request, question_id):
#   if request.method == 'GET':
#     queryset = get_object_or_404(AnswerSmcq, pk=question_id.upper())
#     data = {
#       'question': queryset.question.url,
#       'creator': queryset.creator.username,
#       'created_at': queryset.created_at,
#       'topic_id': queryset.topic_id.id,
#       'correct_option': queryset.correct_option,
#     }
#     return JsonResponse(data)



# def GetMmcq(request, question_id):
#   if request.method == 'GET':
#     queryset = get_object_or_404(AnswerMmcq, pk=question_id.upper())
#     data = {
#       'question': queryset.question.url,
#       'creator': queryset.creator.username,
#       'created_at': queryset.created_at,
#       'topic_id': queryset.topic_id.id,
#       'is_O1_correct': queryset.is_O1_correct,
#       'is_O2_correct': queryset.is_O2_correct,
#       'is_O3_correct': queryset.is_O3_correct,
#       'is_O4_correct': queryset.is_O4_correct,
#     }
#     return JsonResponse(data)
  
# def GetIntegerType(request, question_id):
#   if request.method == 'GET':
#     queryset = get_object_or_404(AnswerIntegerType, pk=question_id.upper())
#     # print(queryset)
#     data = {
#       'question': queryset.question.url,
#       'creator': queryset.creator.username,
#       'created_at': queryset.created_at,
#       'topic_id': queryset.topic_id.id,
#       'correct_answer': queryset.correct_answer
#     }
#     return JsonResponse(data)
  

{
# class ListTopics(APIView):
#   def get(self, request, format=None):
#     for chapter in chapters:
#       data={}
#       # querying to get topic list for this chapter
#       chapters_qs = get_object_or_404(Chapter, chapter_name__iexact=chapter)
#       chapter_id = chapters_qs.id
#       topics = Topic.objects.filter(chapter_id=chapter_id)
      
#       # chapter_serializer = ChapterSerializer(chapter)
#       data[chapters_qs.chapter_name]={}
#       # adding each topic now
#       for topic in topics:
#         # topic serializer
#         serializer = TopicSerializer(topic)
#         extracted_data = serializer.data
#         data[chapters_qs.chapter_name][topic.topic_name] = {serializer}
#       print(data)
      
#     queryset = Topic.objects.all()
#     serializer = TopicSerializer(queryset, many=True)
#     return Response(serializer.data, status=status.HTTP_200_OK)
    #####################################################################
    
    # chapters = get_object_or_404(Chapter, pk=id)
    # queryset = Topic.objects.all()
    # serializer = TopicSerializer(queryset, many=True)     # many true means array of json format
    
    # # trying to get chapter name from chapter_id
    # id = serializer.data[0]['chapter_id']
    # queryset = get_object_or_404(Chapter, pk=id)
    # chapter_name = ChapterSerializer(queryset).data['chapter_name']       # json format

    # # reforming data
    # data = serializer.data
    # data[0]['chapter_name'] = chapter_name
    
    # return Response(data, status=status.HTTP_200_OK)
    
###############

}

class ViewQuestionImage(APIView):
  def get(self, request, image_name):
    full_path = f'media/questions/{image_name}'
    return FileResponse(open(full_path, 'rb'))
  
class ViewExplanationImage(APIView):
  def get(self, request, image_name):
    full_path = f'media/explanations/{image_name}'
    return FileResponse(open(full_path, 'rb'))
  
class ViewIcon(APIView):
  def get(self, request, image_name):
    full_path = f'media/icons/{image_name}'
    print(full_path)
    return FileResponse(open(full_path, 'rb'))
