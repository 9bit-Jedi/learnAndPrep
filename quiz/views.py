import json
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import Http404, HttpResponse
from django.core.exceptions import ValidationError
from django.db import IntegrityError 

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework_simplejwt.backends import TokenBackend
from rest_framework.permissions import IsAuthenticated

from questions.models import Chapter, Question, AnswerIntegerType, AnswerMmcq, AnswerSmcq, AnswerSubjective
from questions.serializers import QuestionSerializer, AnswerMmcqSerializer, AnswerIntegerTypeSerializer, AnswerSmcqSerializer, AnswerSubjectiveSerializer

from .models import Quiz, QuizQuestion, QuizQuestionAttemptMmcq, QuizQuestionAttemptInt, QuizQuestionAttemptSmcq
from .serializers import QuizSerializer, QuizQuestionAttemptIntSerializer, QuizQuestionAttemptMmcqSerializer, QuizQuestionAttemptSmcqSerializer

# Create your views here.
class GetQuiz(APIView):
  def get(self, request, format=None):
    queryset = Quiz.objects.all()
    serializer = QuizSerializer(queryset, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
  
class GetAnswer(APIView):
  # permission_classes = [IsAuthenticated]
  def get(self, request, question_id, format=None):
    
    ## only question with that question id
    question = get_object_or_404(Question, id=question_id)

    # queryset=None
    if question.type == 'SMCQ':
      queryset = AnswerSmcq.objects.get(question_id=question_id.upper())
      serializer = AnswerSmcqSerializer(queryset)
    elif question.type == 'MMCQ':
      queryset = AnswerMmcq.objects.get(question_id=question_id.upper())
      serializer = AnswerMmcqSerializer(queryset)
    elif question.type == 'INT':
      queryset = AnswerIntegerType.objects.get(question_id=question_id.upper())
      serializer = AnswerIntegerTypeSerializer(queryset)
    elif question.type == 'SUBJ':
      queryset = AnswerSubjective.objects.get(question_id=question_id.upper())
      serializer = AnswerSubjectiveSerializer(queryset)
    else:
      return Response({'this question type does not have an answer yet.'}, status=status.HTTP_200_OK)
    
    return Response(serializer.data, status=status.HTTP_200_OK)

  def post(self, request, question_id, format=None):
    
    expected_format = {
      'SMCQ': {'marked_option': 'A'},
      'MMCQ': {'is_O1_marked': True, 'is_O2_marked': False, 'is_O3_marked': True, 'is_O4_marked': False},
      'INT': {'marked_answer': 42},
      'SUBJ': {}  # No request body for subjective questions
    }
    
    if request.method == 'POST':
      try:
        # getting details of question and user
        question = get_object_or_404(Question, id=question_id)
        user_id = request.user
        chapter_id = Chapter.objects.get(id=question.chapter_id.id)
        print(question.id)
        
        # creating quiz and quiz question object (if not existing already)
        try:
          quiz = Quiz.objects.get(chapter_id=chapter_id, user_id=user_id) # add try except for total questions and id, solved_questions = 0 default
          print(f"quiz already exists - {quiz.id}")
        except Quiz.DoesNotExist:
          quiz = Quiz.objects.create(
            id=f"{chapter_id}Q", 
            chapter_id=chapter_id, 
            user_id=user_id, 
            module_total_questions=0, module_solved_questions=0,
            main_total_questions=0, main_solved_questions=0,
            adv_total_questions=0, adv_solved_questions=0,
            )
          quiz.save()
          print(f"created quiz for chapter id : {chapter_id}")       # if created an chapter-quiz
        
        quiz_question = QuizQuestion.objects.get_or_create(quiz_id=quiz, question_id=question)[0]
        
        # QuizQuestionAttempt logic:
          # get answer_id using quiz_question_id.question_id.question_answer(reverse relation)
          # check for question type and opens if statements
            # get marked_answer
            # check if the answer is_correct using correct_answer from answer_id
        
        print(quiz_question)
        question = quiz_question.question_id
        type = question.type
        print(type)
        
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        
        # Single Correct
        
        if question.type=='SMCQ':
          print("checking if the SMCQ answer is correct")
          answer = AnswerSmcq.objects.get(question_id=question)
          is_correct=True if body['marked_option'] == answer.correct_option else False
          print(f"SMCQ is correct : {is_correct}")
          try:
            quiz_question_attempt = QuizQuestionAttemptSmcq.objects.create(id="1", quiz_question_id = quiz_question, is_correct=is_correct, marked_option=body['marked_option'], answer_id=answer)
          except IntegrityError as e:
            return HttpResponse({f"Question is already attempted : {e}"}, status=status.HTTP_200_OK)
          #   quiz_question_attempt = QuizQuestionAttemptSmcq.objects.get(quiz_question_id=quiz_question)
          serializer = QuizQuestionAttemptSmcqSerializer(quiz_question_attempt)
          # print(serializer)
          
        # Multiple Correct 
        
        elif question.type=='MMCQ':
          print("checking if the MMCQ answer is correct")
          answer = AnswerMmcq.objects.get(question_id=question)
          is_correct = True
          if body['is_O1_marked'] != answer.is_O1_correct :
            is_correct=False 
          if body['is_O2_marked'] != answer.is_O2_correct :
            is_correct=False 
          if body['is_O3_marked'] != answer.is_O3_correct :
            is_correct=False 
          if body['is_O4_marked'] != answer.is_O4_correct :
            is_correct=False 
          print(f"MMCQ is correct : {is_correct}")
          try:
            quiz_question_attempt = QuizQuestionAttemptMmcq.objects.create(id="1", quiz_question_id = quiz_question, is_correct=is_correct, is_O1_marked=body['is_O1_marked'], is_O2_marked=body['is_O2_marked'], is_O3_marked=body['is_O3_marked'], is_O4_marked=body['is_O4_marked'], answer_id=answer)
          except IntegrityError as e:
            return HttpResponse({f"Question is already attempted : {e}"}, status=status.HTTP_200_OK)
          #   quiz_question_attempt = QuizQuestionAttemptMmcq.objects.get(quiz_question_id=quiz_question)
          serializer = QuizQuestionAttemptMmcqSerializer(quiz_question_attempt)
          # print(serializer)
          
        # Integer type
        
        elif question.type=='INT':
          print("checking if the integer answer is correct")
          answer = AnswerIntegerType.objects.get(question_id=question)
          is_correct=True if body['marked_answer'] == answer.correct_answer else False
          print(is_correct)
          
          try:
            quiz_question_attempt = QuizQuestionAttemptInt.objects.create(id="1", quiz_question_id = quiz_question, is_correct=is_correct, marked_answer=body['marked_answer'], answer_id=answer)
          except IntegrityError as e:
            return HttpResponse({f"Question is already attempted : {e}"}, status=status.HTTP_200_OK)
          #   quiz_question_attempt = QuizQuestionAttemptSmcq.objects.get(quiz_question_id=quiz_question)
                    
          serializer = QuizQuestionAttemptIntSerializer(quiz_question_attempt)
          # print(serializer)
          
        # Subjective Type 
          
        elif question.type=='SUBJ':
          print("nothing to check for in subjective.")
          answer=AnswerSubjective.objects.get(question_id=question)
          print(answer)
          serializer = AnswerSubjectiveSerializer(answer)
          
        else:
          print('wrong question type nigga !')
          return HttpResponse({f"we dont support checking this type ({type}) of question yet."}, status=status.HTTP_200_OK)
      
      # handling errors : 
      except json.JSONDecodeError as e:
        return Response({
            'error': 'Invalid JSON format',
            'details': str(e),
            'expected_format': expected_format.get(question.type, {}) 
        }, status=status.HTTP_400_BAD_REQUEST)

      except KeyError as e:
        return Response({
          'error': f'Missing key in request body: {e}',
          'expected_keys': list(expected_format.get(question.type, {}).keys())
        }, status=status.HTTP_400_BAD_REQUEST)

      except IntegrityError as e:
        return HttpResponse({f"Question is already attempted : {e}"}, status=status.HTTP_200_OK)

      except Exception as e:
        return HttpResponse(f"An error occurred: {e}", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

      
      return Response(serializer.data, status=status.HTTP_201_CREATED)