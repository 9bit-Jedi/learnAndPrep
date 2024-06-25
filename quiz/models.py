from django.db import models
# from django.conf import settings
# User = settings.AUTH_USER_MODEL
from accounts.models import User

from questions.models import Chapter, Question, AnswerSmcq, AnswerMmcq, AnswerIntegerType

# Create your models here.

class Quiz(models.Model):
  id = models.CharField(max_length=50, primary_key=True)
  chapter_id = models.ForeignKey(Chapter, on_delete=models.CASCADE)
  user_id = models.ForeignKey(User, on_delete=models.CASCADE)
  
  module_total_questions = models.IntegerField()
  module_solved_questions = models.IntegerField(default=0)
  
  main_total_questions = models.IntegerField()
  main_solved_questions = models.IntegerField(default=0)
  
  adv_total_questions = models.IntegerField()
  adv_solved_questions = models.IntegerField(default=0)
  
  def calc_total(self):
    return QuizQuestion.objects.filter(quiz_id=self.id).count()
  
  def save(self, *args, **kwargs):
    self.module_total_questions=Question.objects.filter(chapter_id=self.chapter_id, source='MODULE').count()
    self.main_total_questions=Question.objects.filter(chapter_id=self.chapter_id, source='MAIN').count()
    self.adv_total_questions=Question.objects.filter(chapter_id=self.chapter_id, source='ADV').count()
    self.id = f"{self.user_id.id}Q{self.chapter_id.id}"
    super().save(*args, **kwargs)
  
  def __str__(self):
      return f"{self.user_id.id} - {self.chapter_id}"

class QuizQuestion(models.Model):
  quiz_id = models.ForeignKey(Quiz, on_delete=models.CASCADE)
  question_id = models.ForeignKey(Question, on_delete=models.CASCADE)
  solved_status = models.BooleanField(default=True)
  
  def __str__(self):
      return f"Quiz {self.quiz_id} | Question {self.question_id.id}"
    
# attempt models

class QuizQuestionAttemptAbstract(models.Model):
  id = models.CharField(max_length=20, primary_key=True)
  quiz_question_id = models.ForeignKey(QuizQuestion, on_delete=models.CASCADE)
  is_correct = models.BooleanField(null=False)
  
  def save(self, *args, **kwargs):
    self.id = f"{self.quiz_question_id.quiz_id.user_id.id}AT{self.quiz_question_id.question_id.id}"
    super().save(*args, **kwargs)
  
  class Meta:
    abstract=True

  def __str__(self):
      return f"Quiz {self.quiz_question_id.quiz_id} | Answer {self.quiz_question_id.question_id.id}"
    
class QuizQuestionAttemptSmcq(QuizQuestionAttemptAbstract):
  OPTION_CHOICES = [('A', 'A'),('B', 'B'),('C', 'C'),('D', 'D'),]
  marked_option = models.CharField(max_length=1,choices=OPTION_CHOICES)  
  answer_id = models.ForeignKey(AnswerSmcq, on_delete=models.CASCADE, null=True)

class QuizQuestionAttemptMmcq(QuizQuestionAttemptAbstract):
  is_O1_marked = models.BooleanField()
  is_O2_marked = models.BooleanField()
  is_O3_marked = models.BooleanField()
  is_O4_marked = models.BooleanField()
  answer_id = models.ForeignKey(AnswerMmcq, on_delete=models.CASCADE, null=True)
  
class QuizQuestionAttemptInt(QuizQuestionAttemptAbstract):
  marked_answer = models.FloatField()
  answer_id = models.ForeignKey(AnswerIntegerType, on_delete=models.CASCADE, null=True)