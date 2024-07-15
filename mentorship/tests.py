from django.test import TestCase
from django.test import Client
from accounts.models import *
from .models import *
from .views import *

# Create your tests here.


class MentorModelTest(TestCase):

  def test_create_mentor(self):
    mentor = Mentor.objects.create(
      id="test_id",
      Name="Test Mentor",
      email="test@example.com",
      mobile_no="1234567890",
      mentor_gender="male",
      IIT="IIT Delhi",
      state="Delhi",
      dropper_status="Dropper",
      medium="English",
      did_you_change="No",
      physics_rank=100,
      chemistry_rank=150,
      maths_rank=50,
    )
