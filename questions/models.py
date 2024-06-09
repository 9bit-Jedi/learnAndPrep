from django.db import models
from django.contrib.auth.models import User
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
    
class Chapter(models.Model):
    id = models.CharField(max_length=4, primary_key=True, validators=[MinLengthValidator(4), RegexValidator(r'^(CH)|(MA)|(PH)\d{2}$', "ID must be of format: Subject Letter + 2 digits")])
    chapter_name = models.CharField(max_length=128)
    subject_id = models.ForeignKey(to=Subject, on_delete=models.CASCADE, null=False)
    
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
        return self.chapter_name
    
class Topic(models.Model):
    id = models.CharField(
        max_length=6,
        primary_key=True,
        validators=[
            MinLengthValidator(6),  
            RegexValidator(
                r'^(CH|MA|PH)\d{4}$',  
                "ID must be of format: Subject Letter (CH, MA, or PH) + 4 digits" 
            )
        ]
    )
    topic_name = models.CharField(max_length=128)
    chapter_id = models.ForeignKey(to=Chapter, on_delete=models.CASCADE, null=False, related_name='topics')
    subject_id = models.ForeignKey(to=Subject, on_delete=models.CASCADE, null=True)
    # total_questions = models.IntegerField(null=True, default=0) #
    # solved_questions = models.IntegerField(null=True, default=0) #
    
    # managers
    # objects = models.Manager() #default manager
    # objects_custom = models.Manager() #my new custom manager
    
    
    # def get_total_question(self):
    #     # count = self.topic_question.all().count()        
    #     # topic_id = Topic.objects_custom.filter(topic_name=self)
    #     topic_id = get_object_or_404(Topic, topic_name__iexact=self).id
    #     count = Question.objects.filter(topic_id=topic_id).count()
    #     return count

    # def get_solved_question(self):
    #     count = Question.objects.filter(topic_id=self, solved_status=True).count()
    #     return count
    
    def __str__(self):
        return self.topic_name

class Question(models.Model):
    
    TYPE_CHOICES = [
        ('SMCQ', 'Single Option Correct'),
        ('MMCQ', 'Multiple Option Correct'),
        ('INT', 'Integer Answer Type'),
        ('MATCH', 'Match the Matrix'),
        ('COMPR', 'Comprehension'),
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
    question = models.CharField(max_length=10000)
    creator = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    # answer = models.OneToOneField(to=AnswerBase, on_delete=models.SET_DEFAULT)
    # solved_status = models.BooleanField(default=False, null=True)
    
    # content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    # object_id = models.PositiveIntegerField()
    # answer = GenericForeignKey('content_type', 'object_id')
    
    # class Meta:
    #     indexes = [
    #         models.Index(fields=["content_type", "object_id"]),
    #     ]

# class AnswerBase(models.Model):
#     # id = models.CharField(max_length=10, primary_key=True)
#     # correct_option = models.CharField(max_length=32)
#     solution = models.ImageField(upload_to='questions/solutions/')
    
#     class Meta:
#         abstract = True
    
OPTIONS = ["A", "B", "C", "D"]
ALL_OP = sorted([(item, item) for item in OPTIONS])

class AnswerSmcq(models.Model):
    id = models.CharField(max_length=10, primary_key=True, editable=False)
    question_id = models.OneToOneField(to = Question, on_delete=models.CASCADE, related_query_name="answer_smcq")
    correct_option = models.CharField(max_length=1, choices=ALL_OP)
    
    def __str__(self):
        return self.question_id.id

class AnswerMmcq(models.Model):
    id = models.CharField(max_length=10, primary_key=True)
    question_id = models.OneToOneField(to = Question, on_delete=models.CASCADE, related_query_name="answer_mmcq")
    is_O1_correct = models.BooleanField(default=False)
    is_O2_correct = models.BooleanField(default=False)
    is_O3_correct = models.BooleanField(default=False)
    is_O4_correct = models.BooleanField(default=False)
    
class AnswerIntegerType(models.Model):
    id = models.CharField(max_length=10, primary_key=True)
    question_id = models.OneToOneField(to = Question, on_delete=models.CASCADE, related_query_name="answer_integer")
    correct_answer = models.IntegerField()
