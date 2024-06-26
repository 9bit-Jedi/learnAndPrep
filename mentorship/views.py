from django.shortcuts import render
import pandas as pd

from django.http import HttpResponse
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
# from rest_framework.decorators import parser_classes
from rest_framework.parsers import FormParser, MultiPartParser

from accounts.models import User

from .models import Mentor, Mentee
from .serializers import MentorSerializer, MenteeSerializer
from .script_inference import main
from .script_train import train

# Create your views here.

def ImportMentor(file_path):
  df = pd.read_csv(file_path, delimiter=',')  # csv to dataframe

  print(df)
  for index, row in df.iterrows():
        
    print('hello, I am single creating a mentor')
    
    try:
      Mentor.objects.get_or_create(
        Name= row['Name'],
        email= row['Email Address'],
        # mobile_no= row['mobile_no'],

        mentor_gender= row['mentor_gender'],

        IIT= row['IIT'],
        state= row['state'],

        dropper_status= row['dropper_status'],
        medium= row['medium'],
        did_you_change= row['did_you_change'],
        
        physics_rank= row['physics_rank'],
        chemistry_rank= row['chemistry_rank'],
        maths_rank= row['maths_rank'],
      )
    except Exception as e:
      print(e)
      print("failed !")
      return HttpResponse({"message":"nahhh ! bad mentor data"}, status=status.HTTP_400_BAD_REQUEST)
  return HttpResponse({"message":"populated all mentors into database successfully"}, status=status.HTTP_201_CREATED)


def SaveMenteeDetails(student_data, user):
  try:
    mentee = Mentee.objects.get(user=user)
    # Update existing mentee's data
    mentee.student_gender = student_data.get('gender')  # Use .get() to handle missing keys
    mentee.state = student_data.get('state')
    mentee.medium = student_data.get('medium')
    mentee.did_you_change = student_data.get('medium_change')
    mentee.physics_rank = student_data.get('physics_rank')
    mentee.chemistry_rank = student_data.get('chemistry_rank')
    mentee.maths_rank = student_data.get('maths_rank')
    mentee.save()
    print("updated")
  except Mentee.DoesNotExist:
    mentee = Mentee.objects.create(
      user= user,
      student_gender= student_data['gender'],
      state= student_data['state'],
      medium= student_data['medium'],
      did_you_change= student_data['medium_change'],
      physics_rank= student_data['physics_rank'],
      chemistry_rank= student_data['chemistry_rank'],
      maths_rank= student_data['maths_rank'],)
    # print(e)
    print("new mentee object created !")
  return mentee


class predictCompatibility(APIView):
  parser_classes = [FormParser, MultiPartParser]
  def post(self, request, format=None):
    
    # MENTOR DATA
    
    queryset = Mentor.objects.all()
    serializer = MentorSerializer(queryset, many=True)
    mentor_data = pd.DataFrame(serializer.data)
    
    # STUDENT DATA
        
    user = request.user
    mentee = SaveMenteeDetails(request.data, user)     # querydict
    
    mentee_data = {
      'student_id': mentee.id,
      'student_name': mentee.user.name,
      'student_dropper': mentee.dropper_status,
      'student_maths_rank': mentee.maths_rank,
      'student_physics_rank': mentee.physics_rank,
      'student_chemistry_rank': mentee.chemistry_rank,
      'student_medium': mentee.medium,
      'student_medium_change': mentee.did_you_change,
      'student_state': mentee.state,
      'student_gender': mentee.student_gender
    }
    print(pd.DataFrame([mentee_data])) 
    alloted_mentor = main(mentee_data, mentor_data)
    
    print(f"\n")
    # testing \
    
    mentee_data2 = {
      'student_id': mentee.id,
      'student_name': "test",
      'student_dropper': "Dropper",
      'student_maths_rank': 2,
      'student_physics_rank': 5,
      'student_chemistry_rank': 4,
      'student_medium': "English",
      'student_medium_change': "NO",
      'student_state': "New Delhi",
      'student_gender': "male" 
    }
    print(pd.DataFrame([mentee_data2])) 
    print(main(mentee_data2, mentor_data))
    
    return Response(alloted_mentor, status=status.HTTP_200_OK)
