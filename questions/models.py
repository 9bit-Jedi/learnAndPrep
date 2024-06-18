from django.db import models
from django.conf import settings
User = settings.AUTH_USER_MODEL

from django.shortcuts import get_object_or_404
from django.core.validators import MinLengthValidator, RegexValidator

# from django.contrib.contenttypes.fields import GenericForeignKey
# from django.contrib.contenttypes.models import ContentType
# from django.contrib.contenttypes.fields import GenericRelation

# Create your models here.
class Subject(models.Model):
    SUBJECT_CHOICES = [
        ('PH', 'Physics'),
        ('CH', 'Chemistry'),
        ('MA', 'Mathematics'),
    ]
    id = models.CharField(max_length=2, primary_key=True)  
    subject_name = models.CharField(max_length=24)
    
    def __str__(self):
        return self.subject_name

class Icon(models.Model):
    id = models.CharField(max_length=4, primary_key=True)
    icon = models.ImageField(upload_to='icons/')

    def __str__(self):
        return self.id
    
class Chapter(models.Model):
    id = models.CharField(max_length=4, primary_key=True, validators=[MinLengthValidator(4), RegexValidator(r'^(CH)|(MA)|(PH)\d{2}$', "ID must be of format: Subject Letter + 2 digits")])
    chapter_name = models.CharField(max_length=128)
    subject_id = models.ForeignKey(to=Subject, on_delete=models.CASCADE, null=False)

    icon_id = models.ForeignKey(to=Icon, on_delete=models.CASCADE)
    
    
    # def save(self, *args, **kwargs):
    #     if not self.id:
    #         last_chapter = Chapter.objects.filter(subject=self.subject).order_by('-id').first()
    #         if last_chapter:
    #             last_number = int(last_chapter.id[2:])
    #         else:
    #             last_number = 0
    #         self.id = f"{self.subject.id}{last_number + 1:02}"
    #     super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.id} - {self.chapter_name}"
    
class Question(models.Model):
    
    TYPE_CHOICES = [
        ('SMCQ', 'Single Option Correct'),
        ('MMCQ', 'Multiple Option Correct'),
        ('INT', 'Integer Answer Type'),
        ('SUBJ', 'Subjective'),
        ('MATCH', 'Match the Matrix'),
    ]
    
    SOURCE_CHOICES = [
        ('MODULE', 'From Nucleus Module'),
        ('MAIN', 'Jee Mains pyq'),
        ('ADV', 'Jee Advance pyq'),
        ('TEST', 'Uploaded for mock test'),
        ('MISSL', 'Missl'),
    ]
    
    id = models.CharField(max_length=9, primary_key=True, validators=[MinLengthValidator(7), RegexValidator(r'^(CH)|(MA)|(PH)\d{5}$', "ID must be of format: Subject Letter + 2 digits")])
    chapter_id = models.ForeignKey(to=Chapter, on_delete=models.CASCADE, null=False, related_name='chapter_questions') #
    type = models.CharField(max_length=128, choices=TYPE_CHOICES)
    source = models.CharField(max_length=128, choices=SOURCE_CHOICES)
    # question = models.CharField(max_length=10000)
    question = models.ImageField(upload_to='')
    creator = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    
OPTION_CHOICES = [('A', 'A'),('B', 'B'),('C', 'C'),('D', 'D'),]

class AbstractAnswer(models.Model):
    id = models.CharField(max_length=8, primary_key=True)
    question_id = models.OneToOneField(Question, on_delete=models.CASCADE, related_query_name="question_answer")
    explanation = models.ImageField(upload_to='explanations/', null=True)
    class Meta:
        abstract = True
    
    def save(self, *args, **kwargs):
        self.id = self.question_id.id + 'A'
        super().save(*args, **kwargs)

    def __str__(self):
        return self.question_id.id

class AnswerSmcq(AbstractAnswer):
    correct_option = models.CharField(max_length=1, choices=OPTION_CHOICES)
    

class AnswerMmcq(AbstractAnswer):
    is_O1_correct = models.BooleanField(default=False)
    is_O2_correct = models.BooleanField(default=False)
    is_O3_correct = models.BooleanField(default=False)
    is_O4_correct = models.BooleanField(default=False)
    
class AnswerIntegerType(AbstractAnswer):
    correct_answer = models.FloatField()
    
class AnswerSubjective(AbstractAnswer):
    correct_answer = models.CharField(max_length=512, null=True)
