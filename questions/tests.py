from django.test import TestCase

# Create your tests here.

from .models import AnswerSmcq
AnswerSmcq.objects.all().delete()