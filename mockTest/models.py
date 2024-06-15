from django.db import models
from django.conf import settings
User = settings.AUTH_USER_MODEL
from django.shortcuts import get_object_or_404
from django.core.validators import MinLengthValidator, RegexValidator

from questions.models import Question

# Create your models here.

class Test(models.Model):
  
  test_instructions = """1. The Test consists of Three Sections:- Physics, Chemistry, Mathematics.

2. Total number of Questions:- 54 (Each section consists of 18 questions).

3 .Each Section consists of Three Sub-Section :- Section A , Section B , Section C

4. Marking Scheme -
For Section A
Integer Type Questions (Single Digit Integer) (8 Questions)
For each Question, enter the correct single digit integer value.
Positive Marks : +3 , Negative Marks : 00

For Section B
One or More than one correct (6 Questions)
For each Question, choose the option(s) corresponding to (all) the correct answers.
Positive Marks : +4 , Negative Marks : -1

For Section C
Single Correct (4 Questions)
For each Question, choose the correct option corresponding to the correct Answer.
Each Question has Four options (1),(2),(3),(4). Only ONE of these options is the correct answer.
Positive Marks : +4 , Negative Marks : -1

5. Test Duration:- 180 mins.

6. Test Timing:- 14:00 PM."""

  id = models.CharField(
    max_length=4, 
    primary_key=True, 
    )
  name = models.CharField(max_length=128)
  duration = models.DurationField(null=False)
  instructions = models.CharField(max_length=1024, default=test_instructions, null=True)
  image_test = models.CharField(max_length=128, null=True, )

  def __str__(self):
      return self.name

class LiveTest(Test):
  start_time = models.DateTimeField()
  
  def __str__(self):
    return self.name

class TestAttempt(models.Model):
  id = models.CharField(
    primary_key=True,
    max_length=10
  )
  user_id = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='user_tests')
  test_id = models.ForeignKey(to=Test, on_delete=models.CASCADE, related_name='test_attempts')

  start_time = models.DateTimeField(auto_now_add=True)
  submission_time = models.DateTimeField(null=True)
  
  score = models.IntegerField(default=0, null=True)
  correct = models.IntegerField(null=True)
  incorrect = models.IntegerField(null=True)
  skipped = models.IntegerField(null=True)
  
  def save(self, *args, **kwargs):
    self.id = f"{self.user_id.username}_{self.test_id.id}"
    super().save(*args, **kwargs)
    
  def __str__(self):
    return f"{self.user_id.username} - {self.test_id.name}"

class TestQuestion(models.Model):

  id = models.CharField(max_length=8, primary_key=True)
  test_id = models.ForeignKey(to=Test, on_delete=models.CASCADE)
  question_id = models.ForeignKey(to=Question, on_delete=models.CASCADE)
  positive_marks = models.IntegerField(default=4)
  negative_marks = models.IntegerField(default=1)
  
  # status = models.CharField(default=False, choices=STATUS_CHOICES, null=True)
  # time_taken = models.BooleanField(default=False, null=True)
  
  def save(self, *args, **kwargs):
    self.id = f"{self.test_id.id}_{self.question_id.id}"
    super().save(*args, **kwargs)
    
class TestQuestionAttempt(models.Model):
  
  STATUS_CHOICES = {
    ('Attempted', 'Attempted'),
    ('Unattempted', 'Unattempted'),
    ('Skipped', 'Skipped'),
  }
  
  id = models.CharField(max_length=50, primary_key=True)
  user_id = models.ForeignKey(to=User, on_delete=models.CASCADE)
  test_attempt_id = models.ForeignKey(to=TestAttempt, on_delete=models.CASCADE)
  test_question_id = models.ForeignKey(to=Question, on_delete=models.CASCADE)
  
  status = models.CharField(max_length=64, choices=STATUS_CHOICES, null=True)
  time_taken = models.BooleanField(default=False, null=True)
  
  def save(self, *args, **kwargs):
    self.id = f"{self.test_id.id}_{self.question_id.id}"
    super().save(*args, **kwargs)