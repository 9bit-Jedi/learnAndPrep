from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

# Create your models here.
OPTIONS = ["A", "B", "C", "D"]
ALL_OP = sorted([(item, item) for item in OPTIONS])

SUBJECTS = ["Physics", "Chemistry", "Maths"]
ALL_SUBS = sorted([(item, item) for item in SUBJECTS])


class Subject(models.Model):
    subject_name = models.CharField(max_length=10, choices=ALL_SUBS)
    
    def __str__(self):
        return self.subject_name
    
class Chapter(models.Model):
    chapter_name = models.CharField(max_length=128)
    subject_id = models.ForeignKey(to=Subject, on_delete=models.CASCADE, null=False)
    
    def __str__(self):
        return self.chapter_name
    
class Topic(models.Model):
    topic_name = models.CharField(max_length=128)
    chapter_id = models.ForeignKey(to=Chapter, on_delete=models.CASCADE, null=False, related_name='topics')
    subject_id = models.ForeignKey(to=Subject, on_delete=models.CASCADE, null=True)
    total_questions = models.IntegerField(null=True) #
    solved_questions = models.IntegerField(null=True) #
    
    #managers
    objects = models.Manager() #default manager
    objects_custom = models.Manager() #my new custom manager
    
    
    def get_total_question(self):
        # count = self.topic_question.all().count()        
        # topic_id = Topic.objects_custom.filter(topic_name=self)
        topic_id = get_object_or_404(Topic, topic_name__iexact=self).id
        # print(topic_id)
        count = Question.objects.filter(topic_id=topic_id).count()
        return count

    def get_solved_question(self):
        count = Question.objects.filter(topic_id=self, solved_status=True).count()
        return count
    
    def __str__(self):
        return self.topic_name
    
    
class Question(models.Model):
    question = models.ImageField(upload_to='questions/images/')
    creator = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    topic_id = models.ForeignKey(to=Topic, on_delete=models.CASCADE, null=False, related_name='topic_questions') #
    solved_status = models.BooleanField(default=False, null=True)

class Smcq(Question):
    correct_option = models.CharField(max_length=1, choices=ALL_OP)

class Mmcq(Question):
    is_O1_correct = models.BooleanField(default=False)
    is_O2_correct = models.BooleanField(default=False)
    is_O3_correct = models.BooleanField(default=False)
    is_O4_correct = models.BooleanField(default=False)
    
class IntegerType(Question):
    correct_answer = models.IntegerField()
