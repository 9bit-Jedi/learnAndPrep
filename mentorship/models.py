from django.db import models
import uuid, hashlib

from accounts.models import User
# Create your models here.

# mentor model - from scratch 

class Mentor(models.Model):
  
  MEDIUM_CHOICES = [('English', 'English'), ('Hindi', 'Hindi')]
  GENDER_CHOICES = [('male', 'male'), ('female', 'female')]
  DROPPER_CHOICES = [('Dropper', 'Dropper'), ('Non-dropper', 'Non-dropper')]
  CHANGE_OPTIONS = [('Yes', 'Yes'), ('No', 'No')]
  
  # id = models.CharField(primary_key=True, max_length=200)
  Name = models.CharField(max_length=50)
  email = models.EmailField(max_length=254)
  # mobile_no = models.models.PhoneNumberField(null=True, blank=True)
  
  mentor_gender = models.CharField(max_length=12, choices=GENDER_CHOICES)
  profile_photo = models.ImageField(upload_to='mentor_pfp/', null=True, blank=True)
  about = models.TextField(max_length=512, null=True, blank=True)
  
  IIT = models.CharField(max_length=48)
  state = models.CharField(max_length=48)
  
  dropper_status = models.CharField(max_length=28, choices=DROPPER_CHOICES)
  medium = models.CharField(choices=MEDIUM_CHOICES, max_length=28)
  did_you_change = models.CharField(choices=CHANGE_OPTIONS, max_length=28)
  # did_you_change = models.BooleanField()
  
  physics_rank = models.IntegerField()
  chemistry_rank = models.IntegerField()
  maths_rank = models.IntegerField()

  def __str__(self):
    return f"{self.id} - {self.Name} - {self.IIT}" 
  
  # def save(self, *args, **kwargs):
  #   self.id = hashlib.sha256(f"{self.Name}{self.IIT}".encode('utf-8')).hexdigest() 
  #   super().save(*args, **kwargs)
  
  
class Mentee(models.Model):
  
  MEDIUM_CHOICES = [('English', 'English'), ('Hindi', 'Hindi')]
  GENDER_CHOICES = [('male', 'male'), ('female', 'female')]
  DROPPER_CHOICES = [('Dropper', 'Dropper'), ('Non-dropper', 'Non-dropper')]
  CHANGE_OPTIONS = [('YES', 'YES'), ('NO', 'NO')]
  
  
  user = models.OneToOneField(to=User,on_delete=models.CASCADE)
  
  student_gender = models.CharField(max_length=12, choices=GENDER_CHOICES)
  # profile_photo = models.ImageField(upload_to='mentor_pfp/', null=True, blank=True)
  # about = models.TextField(max_length=512, null=True, blank=True)
  
  state = models.CharField(max_length=48)
  
  dropper_status = models.CharField(max_length=28, choices=DROPPER_CHOICES)
  medium = models.CharField(choices=MEDIUM_CHOICES, max_length=28)
  did_you_change = models.CharField(choices=CHANGE_OPTIONS, max_length=28)
  
  physics_rank = models.IntegerField()
  chemistry_rank = models.IntegerField()
  maths_rank = models.IntegerField()

  def __str__(self):
    return f"{self.id} - {self.user.name}" 
  
  def save(self, *args, **kwargs):
    # check dropper status using User model
    self.dropper_status = 'Dropper' if self.user.student_class == "11th" or "12th" else "Non-dropper"
    super().save(*args, **kwargs)