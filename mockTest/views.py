import json
from django.shortcuts import render, get_object_or_404
from django.http import Http404, HttpResponse
from django.core.exceptions import ValidationError
# from django.db import IntegrityError 

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status, permissions
from rest_framework.permissions import IsAuthenticated
from accounts.permissions import IsPaymentDone, IsMentorAlloted

# from questions.models import Chapter, Question, AnswerIntegerType, AnswerMmcq, AnswerSmcq, AnswerSubjective
# from questions.serializers import QuestionSerializer, AnswerMmcqSerializer, AnswerIntegerTypeSerializer, AnswerSmcqSerializer, AnswerSubjectiveSerializer

from .models import *
from .serializers import *

# Create your views here.

      
class AvailableTestsList(APIView):
    # permission_classes = [IsAuthenticated, IsPaymentDone]  # Uncomment to require authentication

    def get(self, request, format=None):
        now = timezone.now()

        # Get live tests that are currently active
        live_tests = LiveTest.objects.all()
        live_test_serialized = LiveTestSerializer(live_tests, many=True).data
        attempted_tests = []
        # Get regular tests (excluding those already attempted by the user)
        if request.user.is_authenticated:
            attempted_tests = TestAttempt.objects.filter(user=request.user)
            
            attempted_tests_ids=[]
            for attempted_test in attempted_tests:
                attempted_tests_ids.append(attempted_test.test.id)
            
            tests = Test.objects.exclude(id__in=live_tests.values_list('id', flat=True)).exclude(id__in=attempted_tests_ids)
        else:
            tests = Test.objects.exclude(id__in=live_tests.values_list('id', flat=True))  # All tests if not authenticated
        test_serialized = TestSerializer(tests, many=True).data
        attempted_test_serialized = TestAttemptSerializer(attempted_tests, many=True).data

        data = {
            'live_tests': live_test_serialized,
            'tests': test_serialized,
            'attempts': attempted_test_serialized,
        }
        
        return Response(data, status=status.HTTP_200_OK)

from datetime import timedelta
import itertools
class CreateRandomTest(APIView):
    # permission_classes = [IsAuthenticated, IsMentorAlloted]

    def post(self, request, format=None):
        test_name = request.data.get('name', None)
        if test_name is None:
            return Response({'error': 'name not provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        test_duration = request.data.get('duration', None)
        test_duration = timedelta(minutes=int(test_duration))
        if test_duration is None:
            return Response({'error': 'duration not provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        test_instructions = Instructions.objects.all().first()
        
        test = Test.objects.create(name=test_name, duration=test_duration)
        test.instructions = test_instructions
        test.save()

        sections_list = request.data.get('sections', [])
        for section, i in zip(sections_list, itertools.count()):
            section_name = section.get('title', None)
            if section_name is None:
                return Response({'error': 'section name not provided'}, status=status.HTTP_400_BAD_REQUEST)
            
            # questions_list = section.get('questions', [])
            test_section = TestSection.objects.create(test=test, title=section_name, order=i)

            # questions_list = Question.objects.all().order_by('?')[:10]
            if section_name.lower() == 'physics':
                questions_list = Question.objects.filter(chapter_id__subject_id__id='PH').order_by('?')[:10]
                print("Physics")
            elif section_name.lower() == 'chemistry':
                questions_list = Question.objects.filter(chapter_id__subject_id__id='CH').order_by('?')[:10]
                print("Chemistry")
            elif section_name.lower() == 'mathematics':
                questions_list = Question.objects.filter(chapter_id__subject_id__id='MA').order_by('?')[:10]
                print("Mathsss")
            else:
                questions_list = Question.objects.all().order_by('?')[:30]
                print("alll l ll ll")

            for question, i in zip(questions_list, itertools.count()):
                TestQuestion.objects.create(section=test_section, question=question, order=i)

        # test.question.add(*Question.objects.all().order_by('?')[:10])
        test_serialized = TestSerializer(test).data
        test_serialized = dict(test_serialized)
        print(type(test_serialized))
        
        sections = TestSection.objects.filter(test=test)
        sections_serialized = TestSectionSerializer(sections, many=True).data
        test_serialized['sections'] = sections_serialized

        # questions = TestQuestion.objects.filter(section__test=test)
        questions = TestQuestion.objects.all()
        questions_serialized = TestQuestionSerializer(questions, many=True).data
        test_serialized['questions'] = questions_serialized

        return Response(test_serialized, status=status.HTTP_201_CREATED)

class StartTest(APIView):
    permission_classes = [IsAuthenticated, IsPaymentDone]

    def post(self, request, test_id, format=None):

        # test_id = request.data.get('test_id', None)
        if test_id is None:
            return Response({'error': 'test_id not provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        test = get_object_or_404(Test, id=test_id)
        if LiveTest.objects.filter(id=test_id).exists():
            test = LiveTest.objects.get(id=test_id)
            if not test.is_active:
                return Response({'error': 'Test is not live'}, status=status.HTTP_400_BAD_REQUEST)
        
        # if test is being resumed - toh i will send the attempt data in response
        question_attempt = TestAttempt.objects.filter(user=request.user, test=test)
        if question_attempt.exists():
            question_attempt = question_attempt.first()
            question_attempt_serialized = TestAttemptSerializer(question_attempt).data
            return Response(question_attempt_serialized, status=status.HTTP_200_OK)
        
        # if test is being started for the first time
        question_attempt = TestAttempt.objects.create(user=request.user, test=test)
        question_attempt_serialized = TestAttemptSerializer(question_attempt).data
        return Response(question_attempt_serialized, status=status.HTTP_201_CREATED)

class SubmitTest(APIView):
    permission_classes = [IsAuthenticated, IsPaymentDone]

    def post(self, request, test_id, format=None):
        # test_id = request.data.get('test_id', None)
        if test_id is None:
            return Response({'error': 'test_id not provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        test = get_object_or_404(Test, id=test_id)
        if LiveTest.objects.filter(id=test_id).exists():
            live_test = LiveTest.objects.get(id=test_id)
            if not live_test.is_active:
                return Response({'error': 'Test is not live'}, status=status.HTTP_400_BAD_REQUEST)
            # edge case if the live test was over before the user submitted ? tb ky krega ??
        
        # BT dedo - if test already attempted
        if TestAttempt.objects.filter(user=request.user, test=test).exists():
            return Response({'error': 'Test already submitted'}, status=status.HTTP_400_BAD_REQUEST)
        else :
            test_attempt = TestAttempt.objects.create(user=request.user, test=test)
        
        serializer = TestSubmissionSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        
        for section in request.data.get('sections', []):
            section = TestSection.objects.filter(test=test, title=section.get('title', None))
            if not section.exists():
                return Response({'error': 'Section not found'}, status=status.HTTP_400_BAD_REQUEST)
            
            section = section.first()
            for question in section.questions.all():
                test_question_id = question.get('test_question')
                selected_option = question.get('selected_option')
                time_taken = question.get('time_taken')

                question_attempt = TestQuestion.objects.filter(section=section, question=question)
                if not question_attempt.exists():
                    return Response({'error': f'Question {test_question_id} not found'}, status=status.HTTP_400_BAD_REQUEST)
                
                question_attempt = question_attempt.first()
                question_attempt_serialized = TestQuestionSerializer(question_attempt).data
                

                question_attempt.is_attempted = True
                question_attempt.save()
                

                # Evaluate if the answer is correct based on the selected option
                correct_option = question_attempt.question.correct_option
                is_correct = (selected_option == correct_option)

                # Update the attempt with the user's selected option, status, and correctness
                question_attempt.status = question.get('status')
                question_attempt.is_correct = is_correct
                question_attempt.time_taken = time_taken
                question_attempt.save()

                question_attempt, created = TestQuestionAttempt.objects.get_or_create(
                    test_attempt=test_attempt,
                    test_question=test_question,
                    defaults={'status': question_data.get('status'), 'time_taken': time_taken}
                )
        ###############################

        for question_attempt in request.data.get('question_attempts', []):
            question_attempt = TestAttempt.objects.filter(user=request.user, test=test)
            if not question_attempt.exists():
                return Response({'error': 'Test not started'}, status=status.HTTP_400_BAD_REQUEST)
            
            question_attempt = question_attempt.first()
            question_attempt_serialized = TestAttemptSerializer(question_attempt).data
            
            question_attempt.is_submitted = True
            question_attempt.save()
        return Response(question_attempt_serialized, status=status.HTTP_200_OK)

class MyResults(APIView):
    permission_classes = [IsAuthenticated, IsPaymentDone]

    def get(self, request, test_id, format=None):
        test = get_object_or_404(Test, id=test_id)
        question_attempt = TestAttempt.objects.filter(user=request.user, test=test)
        if not question_attempt.exists():
            return Response({'error': 'Test not started'}, status=status.HTTP_400_BAD_REQUEST)
        
        question_attempt = question_attempt.first()
        question_attempt_serialized = TestAttemptSerializer(question_attempt).data
        return Response(question_attempt_serialized, status=status.HTTP_200_OK)