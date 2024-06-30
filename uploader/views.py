import re
import pandas as pd
from django import views
from django.http import HttpResponse
from django.db import IntegrityError, transaction
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
# from rest_framework import viewsets
from django.core.files.images import ImageFile

from accounts.models import User
from accounts.permissions import IsPaymentDone, IsMentorAlloted
from rest_framework.permissions import AllowAny

from questions.models import Subject, Chapter, Question, Icon, AnswerIntegerType, AnswerMmcq, AnswerSmcq, AnswerSubjective
from questions.serializers import SubjectSerializer, ChapterSerializer
from mentorship.views import ImportMentor

from .models import File, Img

# Create your views here.

class ImageUploadView(APIView):
  parser_classes = [MultiPartParser, FormParser]
  permission_classes = [AllowAny]
    
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

class CsvUploadView(APIView):
  parser_classes = [MultiPartParser, FormParser]
  permission_classes = [AllowAny]

  def post(self, request, format=None):    
    file = request.data['csv']
    obj = File.objects.create(file=file)
    
    # checks for content type
    print(request.data['contentType'])
    
    if(request.data['contentType']=='subject'):
      return ImportSubject(obj.file.path)
    elif(request.data['contentType']=='chapter'):
      return ImportChapter(obj.file.path)
    elif(request.data['contentType']=='question'):
      return ImportQuestion(obj.file.path)
    elif(request.data['contentType']=='answer'):
      return ImportAnswer(obj.file.path)
    elif(request.data['contentType']=='mentor'):
      return ImportMentor(obj.file.path)
    # passing file object to Import function


def ImportSubject(file_path):
  # read csv
  try:
    df = pd.read_csv(file_path, delimiter=',')
  except FileNotFoundError:
    return HttpResponse({'error': "File not found."}, status=status.HTTP_400_BAD_REQUEST)
  except pd.errors.EmptyDataError:  
    return HttpResponse({'error': "File is empty."}, status=status.HTTP_400_BAD_REQUEST)
  except pd.errors.ParserError:
    return HttpResponse({'error': "Error parsing the CSV file."}, status=status.HTTP_400_BAD_REQUEST)

  model_instances = []
  invalid_rows = []
  for index, row in df.iterrows():
    subject_data = {
      'id': row['id'],
      'subject_name': row['subject_name']
    }

    serializer = SubjectSerializer(data=subject_data)
    if serializer.is_valid():
      model_instances.append(Subject(**serializer.validated_data))
    else:
      invalid_rows.append({'row':index, 'error':serializer.errors})  # Handle any validation errors here
  
  # bulk create all instances
  try:
    with transaction.atomic():
      Subject.objects.bulk_create(model_instances)
  except IntegrityError as e:
    return HttpResponse({'error':f"Integrity Error : {e}"}, status=status.HTTP_400_BAD_REQUEST)
  
  return HttpResponse({'messsage':"success"}, status=status.HTTP_201_CREATED)

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
    
    # print('hello, I am single creating a chapter')
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
  creator = User.objects.get(name='utsah')
  # print("df created !")
  
  invalid_rows = []
  
  for index, row in df.iterrows():
    question_id = row['question_id']
    # subject_id = Subject.objects.get(id=question_id[0:2])
    try:
      chapter_id = Chapter.objects.get(id=question_id[0:4])
    except Chapter.DoesNotExist as e:
      invalid_rows.append({'row':index, 'error': f"Chapter id not found : {e}"})
      
    print(row['question_id'])
    if Question.objects.filter(id=row['question_id']).count():
      continue;
    
    try:
      image = ImageFile(open(row['image_path'], 'rb'))
    except FileNotFoundError:
      invalid_rows.append({'row':index, 'error': f"image file not found : {e}"})
      # return HttpResponse({'error': "question image file not found."}, status=status.HTTP_404_NOT_FOUND)
  
    try:
      Question.objects.create(
        id= row['question_id'],
        chapter_id= chapter_id,
        type= row['type'],
        source= row['source'],
        question= image,
        creator= creator
      )
      print(f"Created question id : {row['question_id']}") 
    except Exception as e:
      print(f"error : {str(e)}")
      invalid_rows.append({'row':index, 'error': f"image file not found : {e}"})
      # return HttpResponse({'error':f"{e}", "invalid_rows" : invalid_rows}, status=status.HTTP_400_BAD_REQUEST)
      
  return HttpResponse({"message":"populated all questions into database successfully", "invalid_rows" : invalid_rows}, status=status.HTTP_201_CREATED)

def ImportAnswer(file_path):
  df = pd.read_csv(file_path, delimiter=',')  # csv to dataframe
  invalid_rows = []
  
  for index, row in df.iterrows():
    question_id = row['question_id']
    # subject_id = Subject.objects.get(id=question_id[0:2])
    try:
      question = Question.objects.get(id=question_id)
    except Question.DoesNotExist as e:
      invalid_rows.append({'row':index, 'error': f"Chapter id not found : {e}"})
    
    # try:
    #   image = ImageFile(open(row['image_path'], 'rb'))
    # except FileNotFoundError:
    #   return HttpResponse({'error': "question image file not found."}, status=status.HTTP_404_NOT_FOUND)
    type = row['type']
    try:
      if type=='SMCQ':
        # if answer object already exists
        print(row['question_id'])
        print(type)
        if AnswerSmcq.objects.filter(question_id=row['question_id']).count():
          continue;
        # if it does not exists create it
        AnswerSmcq.objects.create(
          id= f"row['question_id']A",
          question_id= question,
          correct_option = row['correct_answer']
        )
        
      if type=='MMCQ':
        # if answer object already exists
        print(row['question_id'])
        print(type)
        if AnswerMmcq.objects.filter(question_id=row['question_id']).count():
          continue;
        # if it does not exists create it
        # write logic for 4 options
        if "A" in row['correct_answer']:
          is_O1_correct = True
        else:
          is_O1_correct = False
        if "B" in row['correct_answer']:
          is_O2_correct = True
        else:
          is_O2_correct = False
        if "C" in row['correct_answer']:
          is_O3_correct = True
        else:
          is_O3_correct = False
        if "D" in row['correct_answer']:
          is_O4_correct = True
        else:
          is_O4_correct = False
        
        AnswerMmcq.objects.create(
          id= f"row['question_id']A",
          question_id= question,
          is_O1_correct = is_O1_correct,
          is_O2_correct = is_O2_correct,
          is_O3_correct = is_O3_correct,
          is_O4_correct = is_O4_correct
        )
        
      if type=='INT':
        # if answer object already exists
        print(row['question_id'])
        print(type)
        if AnswerIntegerType.objects.filter(question_id=row['question_id']).count():
          continue;
        # if it does not exists create it
        AnswerIntegerType.objects.create(
          id= f"row['question_id']A",
          question_id= question,
          correct_answer = row['correct_answer']
        )
        
      if type=='SUBJ':
        # if answer object already exists
        print(row['question_id'])
        print(type)
        if AnswerSubjective.objects.filter(question_id=row['question_id']).count():
          continue;
        # if it does not exists create it
        AnswerSubjective.objects.create(
          id= f"row['question_id']A",
          question_id= question,
          correct_answer = row['correct_answer']
        )
      print(f"answer id : {row['question_id']}A") 
      print(type)
    except Exception as e:
      print(f"error : {str(e)}")
      return HttpResponse({'error':f"{e}"}, status=status.HTTP_400_BAD_REQUEST)
      
  return HttpResponse({"message":"populated all questions into database successfully"}, status=status.HTTP_201_CREATED)