from django.db import models
from django.contrib.auth.models import User

# Create your models here.
OPTIONS = ["A", "B", "C", "D"]
ALL_OP = sorted([(item, item) for item in OPTIONS])

SUBJECTS = ["Physics", "Chemistry", "Maths"]
ALL_SUBS = sorted([(item, item) for item in SUBJECTS])


class Subject(models.Model):
    value = models.CharField(max_length=10, choices=ALL_SUBS)
    
    def __str__(self):
        return self.value
    
class Chapter(models.Model):
    value = models.CharField(max_length=20)
    subject_id = models.ForeignKey(to=Subject, on_delete=models.CASCADE, null=False)
    
    def __str__(self):
        return self.value
    
class Topic(models.Model):
    value = models.CharField(max_length=20)
    chapter_id = models.ForeignKey(to=Chapter, on_delete=models.CASCADE, null=False)
    
    def __str__(self):
        return self.value
    
    
class Smcq(models.Model):
    question = models.ImageField(upload_to='questions/images/')
    correct_option = models.CharField(max_length=1, choices=ALL_OP)
    creator = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    topic_id = models.ForeignKey(to=Topic, on_delete=models.CASCADE, null=False)
    