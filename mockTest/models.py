from shortuuid.django_fields import ShortUUIDField

from django.utils import timezone
from django.db import models
# from django.conf import settings
# User = settings.AUTH_USER_MODEL
from accounts.models import User
from django.shortcuts import get_object_or_404
from django.core.validators import MinLengthValidator, RegexValidator

from questions.models import Question, Icon, Chapter

# Create your models here.


class Instructions(models.Model):
  id = ShortUUIDField(primary_key=True, editable=False, max_length=22)
  test_syllabus = models.TextField(max_length=1024)
  general_instructions = models.TextField(max_length=1024)
  # navigating_to_a_question = models.TextField(max_length=1024)
  navigation_instructions = models.TextField(max_length=1024)
  answering_a_question = models.TextField(max_length=1024)
  declaration = models.TextField(max_length=1024)


  # def __str__(self):
  #   return f"Instructions for Test ID: {self.id}"  # More informative string representation

class TestSeries(models.Model):
  id = ShortUUIDField(primary_key=True, editable=False, max_length=22)
  name = models.CharField(max_length=128)
  description = models.TextField(max_length=1024, blank=True)
  # icon - fk to questions.models.icon
  icon = models.ForeignKey(to=Icon, null=True, on_delete=models.SET_NULL)
  
  def __str__(self):
    return self.name

class Test(models.Model):
  
  id = ShortUUIDField(max_length=22, editable=False, primary_key=True)
  name = models.CharField(max_length=128)
  series = models.ForeignKey(TestSeries, on_delete=models.DO_NOTHING, related_name='tests')
  creator = models.ForeignKey(to=User, null=True, on_delete=models.SET_NULL)
  duration = models.DurationField()
  instructions = models.ForeignKey(to=Instructions, null=True, on_delete=models.SET_NULL)
  # icon - fk to questions.models.icon
  icon = models.ForeignKey(to=Icon, null=True, on_delete=models.SET_NULL)
    
  def __str__(self):
      return f"{self.series} - {self.name}"

class LiveTest(Test):
  start_time = models.DateTimeField()   # has to be set beforehand # views have to check if the test attempt is valid or not (also list test should show 'live' test ka availability )
  end_time = models.DateTimeField(blank=True)   
  
  @property
  def is_active(self):
    now = timezone.now()
    return self.start_time <= now <= self.end_time

  @property
  def status(self):
    now = timezone.now()
    if now < self.start_time:
      return "Upcoming"
    elif self.start_time <= now <= self.end_time:
      return "Live"
    else:
      return "Ended"

  def save(self, *args, **kwargs):
    if not self.end_time:
      self.end_time = self.start_time + self.duration
    super().save(*args, **kwargs)

class CustomTest(Test):
  start_time = models.DateTimeField(blank=True)   # has to be set beforehand # views have to check if the test attempt is valid or not (also list test should show 'live' test ka availability )
  end_time = models.DateTimeField(blank=True)
  syllabus = models.ManyToManyField(to=Chapter, related_name='tests')

class TestSection(models.Model):

  id = ShortUUIDField(primary_key=True, editable=False, max_length=22)
  test = models.ForeignKey(to=Test, on_delete=models.CASCADE, related_name='sections')
  title = models.CharField(max_length=64)
  order = models.PositiveIntegerField()
    
  # def save(self, *args, **kwargs):
  #   self.id = f"{self.test.id}_{self.question.id}"
  #   super().save(*args, **kwargs)
  
  class Meta:
      unique_together = ('test', 'order')
      
  def __str__(self):
    return f"{self.test.name} - {self.title}"
  

class TestQuestion(models.Model):

  id = ShortUUIDField(primary_key=True, editable=False, max_length=22)

  # test = models.ForeignKey(to=BaseTest, on_delete=models.CASCADE, related_name='questions')
  section = models.ForeignKey(to=TestSection, on_delete=models.CASCADE, related_name='questions', null=True)  
  question = models.ForeignKey(to=Question, on_delete=models.CASCADE)

  order = models.PositiveIntegerField()

  positive_marks = models.IntegerField(default=4)
  negative_marks = models.IntegerField(default=1)
    
  # def save(self, *args, **kwargs):
  #   self.id = f"{self.section.test.name}_{self.question.id}"
  #   super().save(*args, **kwargs)
    
  class Meta:
    # unique_together = ('test', 'order')
    ordering = ['order']
  
  # def __str__(self):
  #   return f"{self.test.name} - Q{self.order} ({self.section}): {self.question.id}"
  

class TestAttempt(models.Model):
  id = ShortUUIDField(primary_key=True, max_length=48, editable=False)
  user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='test_attempts')
  test = models.ForeignKey(to=Test, on_delete=models.CASCADE, related_name='test_attempts')

  start_time = models.DateTimeField(auto_now_add=True)
  is_submitted = models.BooleanField(default=False)
  submission_time = models.DateTimeField(null=True, blank=True)   # evaluated_at
  
  score = models.IntegerField(default=0, null=True)
  # correct = models.IntegerField(null=True)
  # incorrect = models.IntegerField(null=True)
  # skipped = models.IntegerField(null=True)
  
  # def correct(self):
  #   return self.get_correct_count()
  # def incorrect(self):
  #   return self.get_incorrect_count()
  # def skipped(self):
  #   return self.get_skipped_count()
  
  def get_correct_count(self):
    return self.question_attempts.filter(is_correct=True, status__in=["Attempted", "SaveMarked"]).count()

  def get_incorrect_count(self):
    return self.question_attempts.filter(is_correct=False, status__in=["Attempted", "SaveMarked"]).count()
  
  def get_skipped_count(self):
    return self.question_attempts.filter(status__in=["Skipped", "Marked"]).count() 

  
  def save(self, *args, **kwargs):
    self.id = f"{self.user.pk}_{self.test.id}"
    # self.correct = self.question_attempts.filter(is_correct=True).count()
    # self.incorrect = self.question_attempts.filter(is_correct=False, status="Attempted").count()
    # self.skipped = self.question_attempts.filter(status="Skipped").count()
    super().save(*args, **kwargs)
    
  def __str__(self):
    return f"{self.user.email} - {self.test.name}"
  
class TestQuestionAttempt(models.Model):
  
  STATUS_CHOICES = {
    ('Attempted', 'Attempted'),
    ('Unattempted', 'Unattempted'),
    ('Skipped', 'not visited'),
    ('Marked', 'Marked for Review'),
    ('SaveMarked', 'Saved and Marked for Review')
  }
  
  id = ShortUUIDField(primary_key=True, editable=False, max_length=48)
  test_attempt = models.ForeignKey(to=TestAttempt, on_delete=models.CASCADE, related_name="question_attempts")
  test_question = models.ForeignKey(to=TestQuestion, on_delete=models.CASCADE) 
  
  # selected_option = models.CharField(max_length=1, choices=Question.OPTION_CHOICES, null=True, blank=True)
  status = models.CharField(max_length=64, choices=STATUS_CHOICES, null=True)
  is_correct = models.BooleanField(default=False)
  time_taken = models.DurationField(null=True)
  
  def save(self, *args, **kwargs):
    if self.time_taken == 0:
      self.status = 'Skipped' 
    super().save(*args, **kwargs)
  
  def __str__(self):
    return f"Test Attempt {self.test_question.section} Q{self.test_question.order}" 