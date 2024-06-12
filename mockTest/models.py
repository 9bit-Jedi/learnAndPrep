from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.core.validators import MinLengthValidator, RegexValidator

from questions.models import Question

# Create your models here.

class Test(models.Model):
  id = models.CharField(
    max_length=4, 
    primary_key=True, 
    validators=[
      MinLengthValidator(4), 
      RegexValidator(r'^(CH)|(MA)|(PH)\d{2}$', "ID must be of format: Subject Letter + 2 digits"
    )])
  name = models.CharField(max_length=128)
  duration = models.DurationField(null=False)

  def __str__(self):
      return self.name
    
# Live Test Model

class LiveTest(Test):
  start_time = models.DateTimeField()
  
  def __str__(self):
    return self.name

# Test attempt model

class TestAttempt(models.Model):
  id = models.CharField(
    primary_key=True,
    max_length=10
  )
  user_id = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='user_tests')
  test_id = models.ForeignKey(to=Test, on_delete=models.CASCADE, related_name='test_attempts')

  start_time = models.DateTimeField(auto_now_add=True)
  submission_time = models.DateTimeField(null=True)
  
  def save(self, *args, **kwargs):
    self.id = self.user_id.id + '_' + self.test_id.id
    super().save(*args, **kwargs)
    
  def __str__(self):
    return self.test_id.name
  

class TestQuestion:
  id = models.CharField(max_length=50)
  test_id = models.ForeignKey(to=Test, on_delete=models.CASCADE)
  question_id = models.ForeignKey(to=Question, on_delete=models.CASCADE)
  
  is_attempted = models.BooleanField(default=False)
  
  def save(self, *args, **kwargs):
    self.id = self.test_id.id + '_' + self.question_id.id
    super().save(*args, **kwargs)