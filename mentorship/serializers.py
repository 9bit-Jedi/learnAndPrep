from rest_framework import serializers
from .models import Mentor, Mentee

# your serializers here
  
class MentorSerializer(serializers.ModelSerializer):
  class Meta:
    model = Mentor
    fields = ('__all__')
    # fields = ('Name','email','mentor_gender','IIT','state','dropper_status','medium','physics_rank','chemistry_rank','maths_rank')

class MenteeSerializer(serializers.ModelSerializer):
  class Meta:
    model = Mentee
    fields = ('__all__')
    # fields = ('Name','email','mentor_gender','IIT','state','dropper_status','medium','physics_rank','chemistry_rank','maths_rank')

