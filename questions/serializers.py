from rest_framework import serializers
from questions.models import Smcq

class QuestionSerializer(serializers.Serializer):
  class Meta:
    model = Smcq
    fields = ('id', 'question', 'correctOptionId')