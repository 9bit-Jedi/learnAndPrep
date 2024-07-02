from django.db import models
import uuid, hashlib

from accounts.models import User
# Create your models here.

# mentor model - from scratch 

max_bandwidth = 5 
class Mentor(models.Model):
  
  MEDIUM_CHOICES = [('English', 'English'), ('Hindi', 'Hindi')]
  GENDER_CHOICES = [('male', 'male'), ('female', 'female')]
  DROPPER_CHOICES = [('Dropper', 'Dropper'), ('Non-dropper', 'Non-dropper')]
  CHANGE_OPTIONS = [('Yes', 'Yes'), ('No', 'No')]
  
  id = models.CharField(primary_key=True, max_length=200)
  Name = models.CharField(max_length=50)
  email = models.EmailField(max_length=254)
  mobile_no = models.CharField(verbose_name="MobileNumber",max_length=15 , null=True)
  
  mentor_gender = models.CharField(max_length=12, choices=GENDER_CHOICES)
  profile_photo = models.ImageField(upload_to='mentor_pfp/', null=True, blank=True)
  about = models.TextField(max_length=2000, null=True, blank=True)
  
  IIT = models.CharField(max_length=48)
  branch = models.CharField(max_length=48, null=True)
  state = models.CharField(max_length=48)
  
  dropper_status = models.CharField(max_length=28, choices=DROPPER_CHOICES)
  medium = models.CharField(choices=MEDIUM_CHOICES, max_length=28)
  did_you_change = models.CharField(choices=CHANGE_OPTIONS, max_length=28)
  # did_you_change = models.BooleanField()
  
  physics_rank = models.IntegerField()
  chemistry_rank = models.IntegerField()
  maths_rank = models.IntegerField()
  
  bandwidth = models.IntegerField(default=0)
  is_available = models.BooleanField(default=True)

  def __str__(self):
    return f"{self.id} - {self.Name} - {self.IIT}" 
  
  def save(self, *args, **kwargs):
    self.bandwidth=self.relationships.count()
    # check if bandwidth <= max_bandwidth
    if self.bandwidth >= max_bandwidth:
      self.is_available = False
    super().save(*args, **kwargs)
  
  
class Mentee(models.Model):
  
  MEDIUM_CHOICES = [('English', 'English'), ('Hindi', 'Hindi')]
  GENDER_CHOICES = [('male', 'male'), ('female', 'female')]
  DROPPER_CHOICES = [('Dropper', 'Dropper'), ('Non-dropper', 'Non-dropper')]
  CHANGE_OPTIONS = [('YES', 'YES'), ('NO', 'NO')]
  
  
  user = models.OneToOneField(to=User,related_name="mentee",on_delete=models.CASCADE)
  
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
    if self.user.student_class in ("11th", "12th"):
      self.dropper_status='Non-dropper'
    else:
      self.dropper_status='Dropper'
    super().save(*args, **kwargs)
    
class MentorMenteeRelationship(models.Model):
  mentee = models.OneToOneField(to=Mentee, related_name="relationships", on_delete=models.CASCADE)
  
  alloted_mentor = models.ForeignKey(to=Mentor, related_name="relationships", on_delete=models.CASCADE)
  alloted_mentor_compatibility = models.FloatField()
   
  extra_mentor_1 = models.ForeignKey(to=Mentor, related_name="relationships_1", on_delete=models.CASCADE)
  extra_mentor_1_compatibility = models.FloatField()
  extra_mentor_2 = models.ForeignKey(to=Mentor, related_name="relationships_2", on_delete=models.CASCADE)
  extra_mentor_2_compatibility = models.FloatField()
  extra_mentor_3 = models.ForeignKey(to=Mentor, related_name="relationships_3", on_delete=models.CASCADE)
  extra_mentor_3_compatibility = models.FloatField()
  
  def __str__(self):
      return f"{self.alloted_mentor.Name} - {self.mentee.user.name}"
  