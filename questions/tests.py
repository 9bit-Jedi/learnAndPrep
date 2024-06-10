from django.test import TestCase

# Create your tests here.

from questions.models import AnswerSmcq, Question
from questions.serializers import AnswerSmcqSerializer

question_id = Question.objects.get(id='MA01002')
AnswerSmcq.objects.create(question_id=question_id, correct_option = 'A')

queryset = AnswerSmcq.objects.all()
serializer = AnswerSmcqSerializer(queryset).data

# Original exception text was: 'QuerySet' object has no attribute 'correct_option'.
# correct_option
# correct_option