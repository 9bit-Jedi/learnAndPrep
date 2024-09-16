from rest_framework import serializers
from accounts.models import User
from .models import (
    Instructions, Test, LiveTest, TestSection, TestQuestion, 
    TestAttempt, TestQuestionAttempt
)
from questions.models import Question, AnswerIntegerType, AnswerMmcq, AnswerSmcq, AnswerSubjective
from questions.serializers import IconSerializer, QuestionSerializer



class InstructionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instructions
        fields = '__all__'
        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [ 'name', 'email']
        
class TestQuestionSerializer(serializers.ModelSerializer):
    question = QuestionSerializer()
    class Meta:
        model = TestQuestion
        fields = '__all__'

class TestSectionSerializer(serializers.ModelSerializer):
    questions = TestQuestionSerializer(many=True)
    class Meta:
        model = TestSection
        fields = '__all__'

class TestSerializer(serializers.ModelSerializer):
  icon = IconSerializer()
  instructions = InstructionsSerializer()
  creator = UserSerializer()
  sections = TestSectionSerializer(many=True)
  class Meta:
      model = Test
      fields = ['id', 'creator', 'name', 'duration', 'instructions', 'icon', 'sections']
      # depth = 1

class LiveTestSerializer(serializers.ModelSerializer):
    icon = IconSerializer()
    instructions = InstructionsSerializer()
    creator = UserSerializer()
    is_active = serializers.BooleanField(read_only=True)  
    sections = TestSectionSerializer(many=True)
 
    class Meta:
        model = LiveTest
        fields = list(TestSerializer.Meta.fields) + ['start_time', 'end_time', 'is_active'] 


class TestAttemptSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    test = TestSerializer()
    correct = serializers.SerializerMethodField()
    incorrect = serializers.SerializerMethodField()
    skipped = serializers.SerializerMethodField()
    
    def get_correct(self, obj):
        return obj.get_correct_count()

    def get_incorrect(self, obj):
        return obj.get_incorrect_count()

    def get_skipped(self, obj):
        return obj.get_skipped_count()

    class Meta:
        model = TestAttempt
        fields = '__all__'

class QuestionSerializer(serializers.ModelSerializer):
    answer = serializers.SerializerMethodField()
    
    def get_answer(self, obj):
        answer_type = obj.type
        if answer_type == "INT":
            answer_obj = AnswerIntegerType.objects.get(question_id=obj.id)
            return AnswerIntegerTypeSerializer(answer_obj).data
        if answer_type == "SMCQ":
            answer_obj = AnswerSmcq.objects.get(question_id=obj.id)
            return AnswerSmcqSerializer(answer_obj).data
        if answer_type == "MMCQ":
            answer_obj = AnswerMmcq.objects.get(question_id=obj.id)
            return AnswerMmcqSerializer(answer_obj).data
        if answer_type == "SUBJ":
            answer_obj = AnswerSubjective.objects.get(question_id=obj.id)
            return AnswerSubjectiveSerializer(answer_obj).data
        else:
            return {}

    class Meta:
        model = Question
        fields = ['id', 'chapter_id', 'type', 'source', 'question', 'answer']

class AnswerIntegerTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnswerIntegerType
        fields = ['correct_answer', 'explanation']

class AnswerSmcqSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnswerSmcq
        fields = ['correct_option', 'explanation']

class AnswerMmcqSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnswerMmcq
        fields = ['is_O1_correct', 'is_O2_correct', 'is_O3_correct', 'is_O4_correct', 'explanation']

class AnswerSubjectiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnswerSubjective
        fields = ['correct_answer', 'explanation']

class TestQuestionAttemptSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestQuestionAttempt
        fields = '__all__'





class TestSubmissionSerializer(serializers.Serializer):
    sections = serializers.ListField(
        child=serializers.DictField(
            child=serializers.ListField(
                child=TestQuestionAttemptSerializer()
            )
        )
    )

# from rest_framework import serializers
# from .models import Test, LiveTest, TestAttempt, TestQuestion
  
# # your serializers here
  
# class TestSerializer(serializers.ModelSerializer):
#   class Meta:
#     model = Test
#     fields = ('__all__')

# class TestAttemptSerializer(serializers.ModelSerializer):
#   # user_id = UserSerializer()
#   test_id = TestSerializer()
  
#   class Meta:
#     model = TestAttempt
#     fields = ('__all__')