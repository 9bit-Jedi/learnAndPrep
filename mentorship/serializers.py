from rest_framework import serializers
from .models import Mentor, Mentee, MentorMenteeRelationship
from accounts.serializers import UserProfileSerializer

from accounts.models import User

# your serializers here
  
class MentorSerializer(serializers.ModelSerializer):
  class Meta:
    model = Mentor
    fields = ('__all__')
    # fields = ('Name','email','mentor_gender','IIT','state','dropper_status','medium','physics_rank','chemistry_rank','maths_rank')

class MenteeSerializer(serializers.ModelSerializer):
  user = UserProfileSerializer()
  class Meta:
    model = Mentee
    fields = ('__all__')
    # fields = ('Name','email','mentor_gender','IIT','state','dropper_status','medium','physics_rank','chemistry_rank','maths_rank')

class MentorMenteeRelationshipSerializer(serializers.ModelSerializer):
  mentee = MenteeSerializer()
  alloted_mentor = MentorSerializer()
  extra_mentor_1 = MentorSerializer()
  extra_mentor_2 = MentorSerializer()
  extra_mentor_3 = MentorSerializer()

  class Meta:
    model = MentorMenteeRelationship
    fields = ('mentee','alloted_mentor','alloted_mentor_compatibility','extra_mentor_1','extra_mentor_1_compatibility','extra_mentor_2','extra_mentor_2_compatibility','extra_mentor_3','extra_mentor_3_compatibility')

class AllotedMentorRelationshipSerializer(serializers.ModelSerializer):
  mentee = MenteeSerializer()
  alloted_mentor = MentorSerializer()

  class Meta:
    model = MentorMenteeRelationship
    # fields = ('__all__')
    fields = ('mentee','alloted_mentor','alloted_mentor_compatibility')
  
class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields=('name', 'mobile_no', 'email', 'student_class', 'is_payment_done', 'is_mentor_alloted')

class MentorSerializer2(serializers.ModelSerializer):
  class Meta:
    model = Mentor
    # fields = ('__all__')
    fields = ('Name','email', 'mobile_no', 'IIT','bandwidth')

class MenteeSerializer2(serializers.ModelSerializer):
  user = UserSerializer()
  class Meta:
    model = Mentee
    # fields = ('__all__')
    fields = ('user',) 

class AllotmentsListSerializer(serializers.ModelSerializer):
  mentee = MenteeSerializer2()
  alloted_mentor = MentorSerializer2()
  class Meta:
    model = MentorMenteeRelationship
    fields=('mentee','alloted_mentor')