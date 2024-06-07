import re
from django import views
from django.http import HttpResponse
from django.db import transaction
from rest_framework import status
# from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView

import csv
import pandas as pd

from questions.models import Subject, Chapter, Topic, Question
from questions.serializers import SubjectSerializer, ChapterSerializer
from .models import File

# Create your views here.

class FileUploadView(APIView):
  parser_classes = [MultiPartParser, FormParser]

  def post(self, request, format=None):    
    file = request.data['csv']
    obj = File.objects.create(file=file)
    
    # checks for content type
    print(request.data['contentType'])
    if(request.data['contentType']=='subject'):
      ImportSubject(obj.file.path)
    elif(request.data['contentType']=='chapter'):
      ImportChapter(obj.file.path)
    # passing file object to ImportSubject function
    
    return HttpResponse(status=status.HTTP_201_CREATED)

def ImportSubject(file_path):
  df = pd.read_csv(file_path, delimiter=',')
  
  model_instances = []
  for index, row in df.iterrows():
    # print(row['id'],row['chapter_name'])
    subject_data = {
      'id': row['id'],
      'subject_name': row['subject_name']
    }

    serializer = SubjectSerializer(data=subject_data)
    if serializer.is_valid():
      model_instances.append(Subject(**serializer.validated_data))
    else:
      print(serializer.errors)  # Handle any validation errors here
  
  # bulk create all instances
  with transaction.atomic():
    Subject.objects.bulk_create(model_instances)

def ImportChapter(file_path):
  df = pd.read_csv(file_path, delimiter=',')  # csv to dataframe
  
  # getting queryset of Subjects for each PH, CH, MA
  try:
    query_PH = Subject.objects.get( id = 'PH' )
    query_CH = Subject.objects.get( id = 'CH' )
    query_MA = Subject.objects.get( id = 'MA' )
  except Subject.DoesNotExist:
    return False, f"Listed Subject not found."
  
  # model_instances = []
  for index, row in df.iterrows():
    
    # dynamically assigning id for each row
    if(row['subject_id']=='PH'): 
      subject_id_fk = query_PH
    elif(row['subject_id']=='CH'): 
      subject_id_fk = query_CH
    elif(row['subject_id']=='MA'): 
      subject_id_fk = query_MA
    
    Chapter.objects.create(
      id= row['id'],
      chapter_name= row['chapter_name'],
      subject_id= subject_id_fk
    )
    # chapter_data = {
    #   'id': row['id'],
    #   'chapter_name': row['chapter_name'],
    #   'subject_id': subject_id_fk
    # }
        
  #   serializer = ChapterSerializer(data=chapter_data)
  #   if serializer.is_valid():
  #     model_instances.append(Chapter(**serializer.validated_data))
  #   else:
  #     print(serializer.errors) 
  
  #   print(serializer)
  # # bulk create all instances
  # with transaction.atomic():
  #   Chapter.objects.bulk_create(model_instances)
    
def ImportTopic(file_path):
  df = pd.read_csv(file_path, delimiter=',')  # csv to dataframe
  
  # getting queryset of Subjects for each PH, CH, MA
  try:
    query_PH = Subject.objects.get( id = 'PH' )
    query_CH = Subject.objects.get( id = 'CH' )
    query_MA = Subject.objects.get( id = 'MA' )
  except Subject.DoesNotExist:
    return False, f"Listed Subject not found."
  
  for index, row in df.iterrows():
    
    chapter_id = row['chapter_id']
    try:
      queryset = Chapter.objects.get( id = chapter_id )
    except Subject.DoesNotExist:
      return False, f"Listed Chapter not found."
  
    Topic.objects.create(
      id= row['id'],
      topic_name= row['topic_name'],
      chapter_id= queryset
    )