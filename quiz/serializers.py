from rest_framework import serializers
from .models import Quiz, QuizQuestion, QuizQuestionAttemptInt, QuizQuestionAttemptMmcq, QuizQuestionAttemptSmcq
from questions.serializers import QuestionSerializer, AnswerIntegerTypeSerializer, AnswerMmcqSerializer, AnswerSmcqSerializer, AnswerSubjectiveSerializer

class QuizSerializer(serializers.ModelSerializer):
  subject_id = serializers.SlugRelatedField(
    read_only=True,
    slug_field='id'
  )
  class Meta:
    model = Quiz
    fields = ('__all__')

class QuizQuestionSerializer(serializers.ModelSerializer):
  # question_id = QuestionSerializer()
  class Meta:
    model = QuizQuestion
    fields = ('id', 'solved_status', 'quiz_id')
    
  def get_image_url(self, question):
    request = self.context.get('request')
    photo_url = question.question.url
    return request.build_absolute_uri(photo_url)
  
# attempt serializers (to be called on checking answer)
class QuizQuestionAttemptSmcqSerializer(serializers.ModelSerializer):
  quiz_question_id = QuizQuestionSerializer()
  answer_id = AnswerSmcqSerializer()
  class Meta:
    model=QuizQuestionAttemptSmcq
    fields = ['id', 'is_correct', 'marked_option', 'quiz_question_id', 'answer_id']
    
class QuizQuestionAttemptMmcqSerializer(serializers.ModelSerializer):
  quiz_question_id = QuizQuestionSerializer()
  answer_id = AnswerMmcqSerializer()
  class Meta:
    model=QuizQuestionAttemptMmcq
    fields = ['id', 'is_correct', 'is_O1_marked', 'is_O2_marked', 'is_O3_marked', 'is_O4_marked', 'quiz_question_id', 'answer_id']
class QuizQuestionAttemptIntSerializer(serializers.ModelSerializer):
  quiz_question_id = QuizQuestionSerializer()
  answer_id = AnswerIntegerTypeSerializer()
  class Meta:
    model=QuizQuestionAttemptInt
    fields = ['id', 'is_correct', 'marked_answer', 'quiz_question_id', 'answer_id']
