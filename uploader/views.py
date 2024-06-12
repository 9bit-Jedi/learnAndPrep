import re
from django import views
from django.http import HttpResponse
from django.db import transaction
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView

import pandas as pd

from questions.models import Subject, Chapter, Question, Icon
from questions.serializers import SubjectSerializer, ChapterSerializer
from .models import File, Img

from django.contrib.auth.models import User

# Create your views here.

class ImageUploadView(APIView):
  parser_classes = [MultiPartParser, FormParser]
    
  def post(self, request, format=None):    
    files = request.FILES.getlist('img')
    print(files)
    if not files :
      return HttpResponse({"error":"no files were selected"}, status=status.HTTP_400_BAD_REQUEST)
    
    
    if(request.data['contentType']=='icon'):
      uploaded_images = []
      for file in files :
        obj = Icon.objects.create(id=f"{file}"[:-4], icon=file)
        uploaded_images.append({
          'id':obj.id,
          'url':obj.icon.url
        })
    
    elif(request.data['contentType']=='question'):
      uploaded_images = []
      for file in files :
        obj = Img.objects.create(file=file)
        uploaded_images.append({
          'id':obj.id,
          'url':obj.file.url
        })
    
    #   print(files)
    #   for file in files:
    #     print(file)
    #     Img.objects.create(icon=file)
        # ImportIcon(obj.file.path)
    #   ImportQuestionImg(obj.file.path)
    # elif(request.data['contentType']=='answer'):
    #   ImportAnswerImg(obj.file.path)
    #   print('done importing questions !')
    # passing file object to ImportSubject function
    
    
    return HttpResponse({
      "message" : "Image uploaded successfully",
      "uploaded_images": uploaded_images  
    },status=status.HTTP_201_CREATED)

# def ImportIcon(file_path):
  
#     Icon.objects.create(
#       id= row['id'],
#     )


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
    elif(request.data['contentType']=='question'):
      ImportQuestion(obj.file.path)
      print('done importing questions !')
    # passing file object to ImportSubject function
    
    return HttpResponse(status=status.HTTP_201_CREATED)

def ImportSubject(file_path):
  df = pd.read_csv(file_path, delimiter=',')
  
  model_instances = []
  for index, row in df.iterrows():
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
  
  for index, row in df.iterrows():
    
    # dynamically assigning id for each row
    if(row['subject_id']=='PH'): 
      subject_id_fk = query_PH
    elif(row['subject_id']=='CH'): 
      subject_id_fk = query_CH
    elif(row['subject_id']=='MA'): 
      subject_id_fk = query_MA
    
    try:
      icon_id = Icon.objects.get(id=row['icon_id'])
    except Icon.DoesNotExist:
      print('listed icon_id does not exist, try uploading icons first')
      return False, f"listed icon_id does not exist, try uploading icons first"
    
    Chapter.objects.create(
      id= row['id'],
      chapter_name= row['chapter_name'],
      subject_id= subject_id_fk, 
      icon_id=icon_id
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
    
def ImportQuestion(file_path):
  df = pd.read_csv(file_path, delimiter=',')  # csv to dataframe
  # print("df created !")
  for index, row in df.iterrows():
    
    # getting queryset
    chapter_id = row['chapter_id']
    try:
      queryset = Chapter.objects.get( id = chapter_id )
    except Chapter.DoesNotExist:
      return False, f"Listed Chapter not found."
  
    creator_id = row['creator']
    try:
      creator_queryset = User.objects.get( username = creator_id )
    except User.DoesNotExist:
      return False, f"Listed Creator not found."

    # print(row['id'])
    # id,type,source,chapter_id,creator,question
    Question.objects.create(
      id= row['id'],
      type= row['type'],
      source= row['source'],
      chapter_id= queryset,
      creator= creator_queryset,
      question= row['question']
    )