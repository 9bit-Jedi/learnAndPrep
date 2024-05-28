from rest_framework import serializers
from questions.models import Smcq, Subject, Chapter, Topic

class SmcqSerializer(serializers.ModelSerializer):
  class Meta:
    model = Smcq
    fields = ('id', 'question', 'correct_option', 'creator', 'created_at', 'topic_id')
    
  def get_image_url(self, smcq):
    request = self.context.get('request')
    photo_url = smcq.question.url
    return request.build_absolute_uri(photo_url)
  
class SubjectSerializer(serializers.ModelSerializer):
  class Meta:
    model = Subject
    fields = ('id', 'value', 'subject_id')
    
    
class ChapterSerializer(serializers.ModelSerializer):
  subject_id = serializers.SlugRelatedField(
    read_only=True,
    slug_field='id'
  )
  class Meta:
    model = Chapter
    fields = ('id', 'value', 'subject_id')

class TopicSerializer(serializers.ModelSerializer):
  chapter_id = serializers.SlugRelatedField(
    read_only=True,
    slug_field='id'
  )
  class Meta:
    model = Topic
    fields = ('id', 'value', 'chapter_id')
    