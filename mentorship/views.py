from django.shortcuts import render
import pandas as pd

from django.http import HttpResponse
from django.db import IntegrityError 
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
# from rest_framework.decorators import parser_classes
from rest_framework.parsers import FormParser, MultiPartParser

from accounts.models import User
from accounts.permissions import IsPaymentDone, IsMentorAlloted

from .models import Mentor, Mentee, MentorMenteeRelationship
from .serializers import MentorSerializer, MenteeSerializer, MentorMenteeRelationshipSerializer, AllotedMentorRelationshipSerializer
from .script_inference import main
from .script_train import train

# Create your views here.

def ImportMentor(file_path):
  df = pd.read_csv(file_path, delimiter=',')  # csv to dataframe

  print(df)
  for index, row in df.iterrows():
        
    print(f"hello, I am single creating a mentor : {row['Name']}")
    
    try:
      Mentor.objects.get_or_create(
        id= row['id'],
        Name= row['Name'],
        email= row['Email Address'],
        mobile_no= row['mobile_no'],
        about= row['about'],
        branch= row['branch'],

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
    print("mentee details updated (if changed)")
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

def SaveRelationshipDetails(mentors, mentee):
  extra_mentors = mentors[1]

  # print ((alloted_mentor))
  alloted_mentor = mentors[0]
  extra_mentor1 = extra_mentors.iloc[0] 
  extra_mentor2 = extra_mentors.iloc[1] 
  extra_mentor3 = extra_mentors.iloc[2] 
  
  try:
    relationship = MentorMenteeRelationship.objects.create(
      mentee = mentee,
      
      alloted_mentor = Mentor.objects.get(id=alloted_mentor['mentor_id']),
      alloted_mentor_compatibility = alloted_mentor['compatibility_score'],
      
      extra_mentor_1 = Mentor.objects.get(id=extra_mentor1['mentor_id']), 
      extra_mentor_1_compatibility = extra_mentor1['compatibility_score'],
      extra_mentor_2 = Mentor.objects.get(id=extra_mentor2['mentor_id']),
      extra_mentor_2_compatibility = extra_mentor2['compatibility_score'],
      extra_mentor_3 = Mentor.objects.get(id=extra_mentor3['mentor_id']),
      extra_mentor_3_compatibility= extra_mentor3['compatibility_score']
    )
    print("saved new allotment : ", relationship)
    return relationship
  except (Mentor.DoesNotExist, IndexError, KeyError, IntegrityError) as e:
    # Handle different types of errors explicitly
    if isinstance(e, Mentor.DoesNotExist):
        error_message = "One or more mentors do not exist."
    elif isinstance(e, IndexError):
        error_message = "Invalid mentor data format."
    elif isinstance(e, KeyError):
        error_message = "Missing mentor ID or compatibility score."
    elif isinstance(e, IntegrityError):
        error_message = "You have already taken the Compatibility Test."
    return (f"{e}", error_message)
   
   
# GET MENTOR VIEW #

class getMentorView(APIView):
  parser_classes = [FormParser, MultiPartParser]
  permission_classes = [IsPaymentDone, IsMentorAlloted]
  
  def get(self, request, format=None):
    
    # STUDENT DATA
    user = request.user
    try:
      mentee = user.mentee
    except Mentee.DoesNotExist as e:
      return Response({"error": "No mentor has been alloted to you.", "error_message": f"Mentor {str(e)}"}, status=status.HTTP_404_NOT_FOUND)
    
    relationship = get_object_or_404(MentorMenteeRelationship, mentee=mentee)
    # relationship = MentorMenteeRelationship.objects.get(mentee=mentee)
    serializer = AllotedMentorRelationshipSerializer(relationship)
    return Response({"message":"Alloted Mentor Details fetched successfully","data":serializer.data}, status=status.HTTP_200_OK)

  
  def post(self, request, format=None):
    
    # MENTOR DATA
    
    queryset = Mentor.objects.filter(is_available=True)
    serializer = MentorSerializer(queryset, many=True)
    mentor_data = pd.DataFrame(serializer.data)
    
    # STUDENT DATA
        
    user = request.user
    mentee = SaveMenteeDetails(request.data, user)     # returned querydict
    
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
    
    # print(pd.DataFrame([mentee_data])) 
    
    mentor = main(mentee_data, mentor_data)     # returned tuple of (dict, df)
    # will save mentor for the sake of bandwidth
    alloted_mentor = Mentor.objects.get(id = mentor[0]['mentor_id'])
    print(alloted_mentor, " - alloted mentor by mentor_id from model")
    # print(mentor[0])
    # print(mentor[1])
    
    try:
      relationship = SaveRelationshipDetails(mentor, mentee)
            
      # if bt with saving MentorMenteeRelationship Model - it already exists (Integrity error) or anything else
      if str(type(relationship)) == r"<class 'tuple'>":
        # replicating  my GET request code in this case
        # user = request.user
        mentee = request.user.mentee

        relationship = get_object_or_404(MentorMenteeRelationship, mentee=mentee)
        # relationship = MentorMenteeRelationship.objects.get(mentee=mentee)
        serializer = MentorMenteeRelationshipSerializer(relationship)
        
        # alloted_mentor.save()
        print(relationship.alloted_mentor,  " - relationship alloted_mentor (already alloted mentor)")
        return Response({"message": "Mentor has already been alloted", "data":serializer.data}, status=status.HTTP_200_OK)
      
      # code if new mentor alloted

      serializer = MentorMenteeRelationshipSerializer(relationship)
      alloted_mentor.save()
      print(alloted_mentor, " - New mentor alloted successfully")
      return Response({"message": "Mentor has been alloted successfully !", "data":serializer.data}, status=status.HTTP_200_OK) 
    
    except IntegrityError as e:
      return Response({"error": "You have already taken the Compatibility Test", "error_message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

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
    
