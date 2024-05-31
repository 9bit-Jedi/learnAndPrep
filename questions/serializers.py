from rest_framework import serializers
from questions.models import Question, Subject, Chapter, Topic, Smcq, Mmcq, IntegerType
  
class SubjectSerializer(serializers.ModelSerializer):
  class Meta:
    model = Subject
    fields = ('id', 'subject_name', 'subject_id')
    
    
class ChapterSerializer(serializers.ModelSerializer):
  subject_id = serializers.SlugRelatedField(
    read_only=True,
    slug_field='id'
  )
  class Meta:
    model = Chapter
    fields = ('id', 'chapter_name', 'subject_id')

class TopicSerializer(serializers.ModelSerializer):
  chapter_id = serializers.SlugRelatedField(
    read_only=True,
    slug_field='id'
  )
  class Meta:
    model = Topic
    fields = ('id', 'topic_name', 'chapter_id')
    

class QuestionSerializer(serializers.ModelSerializer):
  class Meta:
    model = Question
    fields = ('id', 'question', 'creator', 'created_at', 'topic_id')
    
  def get_image_url(self, smcq):
    request = self.context.get('request')
    photo_url = smcq.question.url
    return request.build_absolute_uri(photo_url)

class SmcqSerializer(QuestionSerializer):
  class Meta:
    model=Smcq
    fields = QuestionSerializer.Meta.fields + ('correct_option',)
    
class MmcqSerializer(QuestionSerializer):
  class Meta:
    model=Mmcq
    fields = QuestionSerializer.Meta.fields + ('correct_options','new')
    
class IntegerTypeSerializer(QuestionSerializer):
  class Meta:
    model=IntegerType
    fields = QuestionSerializer.Meta.fields + ('correct_answer','new')


class ChapterSerializer_Nested(serializers.ModelSerializer):
    topics = TopicSerializer(many=True, read_only=True)  # Nested serializer for topics
    class Meta:
        model = Chapter
        fields = ['id', 'chapter_name', 'subject_id', 'topics']