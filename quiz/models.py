from django.db import models
from django.conf import settings
User = settings.AUTH_USER_MODEL

from questions.models import Chapter, Question, AnswerSmcq, AnswerMmcq, AnswerIntegerType

# Create your models here.

class Quiz(models.Model):
  id = models.CharField(max_length=50, primary_key=True)
  chapter_id = models.OneToOneField(Chapter, on_delete=models.CASCADE)
  user_id = models.ForeignKey(User, on_delete=models.CASCADE)
  total_question = models.IntegerField()
  solved_question = models.IntegerField()
  
  def calc_total(self):
    return QuizQuestion.objects.filter(quiz_id=self.id).count()
  
  def __str__(self):
      return f"Chapter ID : {self.chapter_id}"

class QuizQuestion(models.Model):
  quiz_id = models.ForeignKey(Quiz, on_delete=models.CASCADE)
  question_id = models.OneToOneField(Question, on_delete=models.CASCADE)
  solved_status = models.BooleanField(default=False)
  
  def __str__(self):
      return f"Quiz ID : {self.quiz_id} | Question ID : {self.question_id}"