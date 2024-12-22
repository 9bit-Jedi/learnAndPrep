from datetime import timedelta
from datetime import datetime
import itertools
import re
import os
import uuid
import pandas as pd
import tempfile
import zipfile
from django import views
from django.http import HttpResponse
from django.db import IntegrityError, transaction
from requests import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
# from rest_framework import viewsets
from django.core.files.images import ImageFile

from accounts.models import User
from accounts.permissions import IsPaymentDone, IsMentorAlloted
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated

from learnAndPrep import settings
from mockTest.models import Instructions, Test, TestQuestion, TestSection, TestSeries
from mockTest.serializers import TestSectionSerializer, TestSerializerFull
from questions.models import Subject, Chapter, Question, Icon, AnswerIntegerType, AnswerMmcq, AnswerSmcq, AnswerSubjective
from questions.serializers import SubjectSerializer, ChapterSerializer
from mentorship.views import ImportMentor

from .models import File, Img
import shutil

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
    # obj = File.objects.create(file=file)
    
    # checks for content type
    print(request.data['contentType'])
    
    try:
      # Temporary file creation (recommended)
      with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        for chunk in file.chunks():
          temp_file.write(chunk)
          temp_file.flush()
          file_path = temp_file.name
          print(file_path)
        try:
          # with open(file_path, 'r') as f:
          #   content = f.read()
          #   print("File content:")
          #   print(content)

        # Try reading the file with pandas
          try:
            df = pd.read_csv(file_path, delimiter=',')
            print("DataFrame content:")
            print(df)
          except Exception as e:
            print("Error reading CSV with pandas:", e)
              


        except FileNotFoundError:
          print('file not found')
          return HttpResponse({'error': "File not found."}, status=status.HTTP_400_BAD_REQUEST)
        except pd.errors.EmptyDataError:  
          print('empty data (file is empty)')
          return HttpResponse({'error': "File is empty."}, status=status.HTTP_400_BAD_REQUEST)
        except pd.errors.ParserError:
          print('parsing error')
          return HttpResponse({'error': "Error parsing the CSV file."}, status=status.HTTP_400_BAD_REQUEST)

      print(df)
        
      if(request.data['contentType']=='subject'):
        return ImportSubject(df)
      elif(request.data['contentType']=='chapter'):
        print("requesting")
        return ImportChapter(df)
      elif(request.data['contentType']=='question'):
        return ImportQuestion(df)
      elif(request.data['contentType']=='answer'):
        return ImportAnswer(df)
      elif(request.data['contentType']=='mentor'):
        return ImportMentor(df)  # Pass DataFrame for processing

    except Exception as e:
      print(e)
      return HttpResponse({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class CreateTestView(APIView):
  parser_classes = [MultiPartParser, FormParser]
  permission_classes = [IsAdminUser]

  def post(self, request, format=None):
    
    series_id = request.data.get('series_id')
    series = TestSeries.objects.get(id=series_id)
    test_name = request.data.get('name', None) 
    
    file = request.data.get('zip')
    print(test_name)
    if test_name is None:
        return Response({'error': 'name not provided'}, status=status.HTTP_400_BAD_REQUEST)
    
    # sorting basic details : 
    #   test series, test name, test duration, test instructions, test sections
    
    test_duration = request.data.get('duration', None)
    test_duration = timedelta(minutes=int(test_duration))
    if test_duration is None:
        return Response({'error': 'duration not provided'}, status=status.HTTP_400_BAD_REQUEST)
    
    test_instructions = Instructions.objects.all().first()
    
    test = Test.objects.create(name=test_name, series=series, duration=test_duration, instructions = test_instructions, creator=request.user)
    ## test = LiveTest.objects.create(name=test_name, duration=test_duration,start_time=timezone.now(), end_time=timezone.now()+test_duration)
    
    
    # temporary directory after unzipping
    with tempfile.TemporaryDirectory() as temp_dir:
      subdir_name = f"temp_{datetime.now().strftime('%Y%m%d%H%M%S')}_{uuid.uuid4().hex}"
      temp_dir = os.path.join('media/', subdir_name)
      
      with zipfile.ZipFile(file, 'r') as zip_ref:
        zip_ref.extractall(os.path.join(temp_dir))
        
        riyal_temp_dir = temp_dir
        temp_dir = os.path.join(temp_dir, os.listdir(temp_dir)[0])
        
        csv_file = [ filename for filename in os.listdir(temp_dir) if filename.endswith( '.csv' ) ][0]
        if csv_file is None:
            return Response({'error': 'CSV file not found'}, status=status.HTTP_400_BAD_REQUEST)

        df = pd.read_csv(os.path.join(temp_dir, csv_file), delimiter=',', encoding='ISO-8859-1')
        # Clean up the dataframe to remove spaces from chapter id
        df['chapter_id'] = df['chapter_id'].str.strip(' ')
        df['source'] = df['source'].str.strip(' ')
        df['file_name'] = df['file_name'].str.strip(' ')
        df['type'] = df['type'].str.strip(' ')
        df['correct_answer'] = df['correct_answer'].str.strip(' ')
        print(df)
        
        df_ph = df[df['chapter_id'].str.contains('PH')]
        df_ch = df[df['chapter_id'].str.contains('CH')]
        df_ma = df[df['chapter_id'].str.contains('MA')]
                
        # populating questions 
        # df -> df(0:25)
        ph_ids = ImportQuestion(df[0:25], f'{temp_dir}')   # (success tuple) returns list of PH question ids
        print(ph_ids)
        
        ch_ids = ImportQuestion(df[25:50], f'{temp_dir}')   # (success tuple) returns list of PH question ids
        print(ch_ids)
        
        ma_ids = ImportQuestion(df[50:75], f'{temp_dir}')   # (success tuple) returns list of PH question ids
        print(ma_ids)
        
        
        shutil.rmtree(riyal_temp_dir)
        
    sections_list = [
      {"title": "Physics"},
      {"title": "Chemistry"},
      {"title": "Mathematics"}
    ]
    print(sections_list)
    
    for section, i in zip(sections_list, itertools.count()):
        section_name = section.get('title', None)
        if section_name is None:
            return Response({'error': 'section name not provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        # questions_list = section.get('questions', [])
        test_section = TestSection.objects.create(test=test, title=section_name, order=i)

        if section_name.lower() == 'physics':
            questions_list = Question.objects.filter(id__in=ph_ids)
            print("Physics")
        elif section_name.lower() == 'chemistry':
            questions_list = Question.objects.filter(id__in=ch_ids)
            print("Chemistry")
        elif section_name.lower() == 'mathematics':
            questions_list = Question.objects.filter(id__in=ma_ids)
            print("Mathsss")
        else:
            questions_list = Question.objects.all().order_by('?')[:25]
            print("alll l ll ll")

        for question, i in zip(questions_list, itertools.count()):
            TestQuestion.objects.create(section=test_section, question=question, order=i)

    # test.question.add(*Question.objects.all().order_by('?')[:10])
    test_serialized = TestSerializerFull(test).data
    test_serialized = dict(test_serialized)
    print(type(test_serialized))
    
    sections = TestSection.objects.filter(test=test)
    sections_serialized = TestSectionSerializer(sections, many=True).data
    test_serialized['sections'] = sections_serialized
        
    return HttpResponse(test_serialized, status=status.HTTP_201_CREATED)



def ImportSubject(df):

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

def ImportChapter(df):
  # df = pd.read_csv(file_path, delimiter=',')  # csv to dataframe
  
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
  return HttpResponse({'message':"populated all chapters into database successfully"}, status=status.HTTP_201_CREATED)


def ImportQuestion(df, temp_path):
  # df = pd.read_csv(file_path, delimiter=',')  # csv to dataframe
  creator = User.objects.get(name='admin')
  print("df created !")
  
  invalid_rows = []
  question_ids = []
  
  for index, row in df.iterrows():
    print(index)
    # if 'question_id' not in row:
    #   return HttpResponse({'error': "CSV file is missing 'question_id' column."}, status=status.HTTP_400_BAD_REQUEST)
    # subject_id = Subject.objects.get(id=question_id[0:2])
    chapter = Chapter.objects.get(id=row['chapter_id'])
    # print(chapter)
    
    # Get the last question id for the given chapter_id
    # last_question = Question.objects.filter(chapter_id=chapter_id).order_by('id').last()
    # if last_question:
    #   last_question_id = last_question.id
    #   new_question_number = int(last_question_id[-2:]) + 1
    #   question_id = f"{chapter_id}{new_question_number}"
    # else:
    #   question_id = f"{chapter_id}01"
    
    try:
      file_path = os.path.join(temp_path, row['file_name'])
      
      # file_path = os.path.join('media/temp/', row['file_name'])
      # if not file_path.startswith(temp_path):
      #   raise ValueError(f"Path traversal detected: {file_path}")
      
      print(file_path)
      image = ImageFile(open(file_path, 'rb'))
    except FileNotFoundError as e:
      invalid_rows.append({'row':index, 'error': f"image file not found : {e}"})
      print("hello",str(e))
      continue
      # return HttpResponse({'error': "question image file not found."}, status=status.HTTP_404_NOT_FOUND)
  
    try:
      question = Question.objects.create(
        # id = question_id,
        chapter_id = chapter,
        type = row['type'],
        source = row['source'],
        question = image,
        creator = creator
      )
      print(f"Created question id : {question.id}") 
      question_ids.append(question.id)
      
      row['question_id'] = question.id
      importAnswer2(row)
    except Exception as e:
      print("hmm ",str(e))
      invalid_rows.append({'row':index, 'error': f"image file not found : {e}"})
      
      # return HttpResponse({'error':f"{e}", "invalid_rows" : invalid_rows}, status=status.HTTP_400_BAD_REQUEST)
  return question_ids
  # return HttpResponse({"message":"populated all questions into database successfully", "invalid_rows" : invalid_rows}, status=status.HTTP_201_CREATED)


def importAnswer2(row):
  
  type = row['type']
  print(row['question_id'])
  question = Question.objects.get(id=row['question_id'])
  try:
    if type=='SMCQ':
      # if answer object already exists
      print(type)
      # if AnswerSmcq.objects.filter(question_id=row['question_id']).count():
        # continue;
      # if it does not exists create it
      AnswerSmcq.objects.create(
        id= f"{row['question_id']}A",
        question_id= question,
        correct_option = row['correct_answer']
      )
      
    if type=='MMCQ':
      # if answer object already exists
      print(type)
      # if AnswerMmcq.objects.filter(question_id=row['question_id']).count():
      #   continue;
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
        id= f"{row['question_id']}A",
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
      # if AnswerIntegerType.objects.filter(question_id=row['question_id']).count():
      #   continue;
      # if it does not exists create it
      AnswerIntegerType.objects.create(
        id= f"{row['question_id']}A",
        question_id= question,
        correct_answer = row['correct_answer']
      )
      
    if type=='SUBJ':
      # if answer object already exists
      print(row['question_id'])
      print(type)
      # if AnswerSubjective.objects.filter(question_id=row['question_id']).count():
      #   continue;
      # if it does not exists create it
      AnswerSubjective.objects.create(
        id= f"{row['question_id']}A",
        question_id= question,
        correct_answer = row['correct_answer']
      )
    print(f"answer id : {row['question_id']}A") 
    print(type)
  except Exception as e:
    print(f"error : {str(e)}")
    



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