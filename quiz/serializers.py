from rest_framework import serializers
from .models import Quiz, QuizQuestion

class QuizSerializer(serializers.ModelSerializer):
  subject_id = serializers.SlugRelatedField(
    read_only=True,
    slug_field='id'
  )
  class Meta:
    model = Quiz
    fields = ('__all__')

class QuizQuestionSerializer(serializers.ModelSerializer):
  class Meta:
    model = QuizQuestion
    fields = ('__all__')
    
  def get_image_url(self, question):
    request = self.context.get('request')
    photo_url = question.question.url
    return request.build_absolute_uri(photo_url)