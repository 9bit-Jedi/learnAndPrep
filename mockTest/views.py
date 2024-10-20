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
from questions.utils import check_answer

from .models import *
from .serializers import *

from datetime import timedelta
import itertools

from django.db import connection
from .utils import QueryLogger
ql = QueryLogger()

# Create your views here.

class AvailableTestSeriesList(APIView):
    # permission_classes = [IsAuthenticated, IsPaymentDone]  # Uncomment to require authentication

    def get(self, request, format=None):
        test_series = TestSeries.objects.all()
        test_series_serialized = TestSeriesSerializer(test_series, many=True).data
        return Response({"success":True, "message":"Test series list fetched successfully", "data":test_series_serialized}, status=status.HTTP_200_OK)

class TestsFromSeriesList(APIView):
    # permission_classes = [IsAuthenticated, IsPaymentDone]  # Uncomment to require authentication

    def get(self, request, series_id, format=None):
        test_series = get_object_or_404(TestSeries, id=series_id)
        tests = Test.objects.filter(series=test_series)
        test_serialized = TestSerializer(tests, many=True).data
        return Response({"success":True, "message":"Test list fetched successfully", "data":test_serialized}, status=status.HTTP_200_OK)

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
        
        return Response({"success":True, "message":"Test list fetched successfully", "data":data}, status=status.HTTP_200_OK)

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
        # test = LiveTest.objects.create(name=test_name, duration=test_duration,start_time=timezone.now(), end_time=timezone.now()+test_duration)
        test.instructions = test_instructions
        test.save()

        sections_list = request.data.get('sections', [])
        for section, i in zip(sections_list, itertools.count()):
            section_name = section.get('title', None)
            if section_name is None:
                return Response({'error': 'section name not provided'}, status=status.HTTP_400_BAD_REQUEST)
            
            # questions_list = section.get('questions', [])
            test_section = TestSection.objects.create(test=test, title=section_name, order=i)

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
        test_serialized = TestSerializerFull(test).data
        test_serialized = dict(test_serialized)
        print(type(test_serialized))
        
        sections = TestSection.objects.filter(test=test)
        sections_serialized = TestSectionSerializer(sections, many=True).data
        test_serialized['sections'] = sections_serialized

        # questions = TestQuestion.objects.filter(section__test=test)
        # questions = TestQuestion.objects.filter(section__test=test)
        # questions = TestQuestion.objects.all()
        # questions_serialized = TestQuestionSerializer(questions, many=True).data

        return Response(test_serialized, status=status.HTTP_201_CREATED)

class StartTest(APIView):
    permission_classes = [IsAuthenticated, IsPaymentDone]

    def post(self, request, test_id, format=None):

        # test_id = request.data.get('test_id', None)
        if test_id is None:
            return Response({'error': 'test_id not provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        if LiveTest.objects.filter(id=test_id).exists():
            test = LiveTest.objects.get(id=test_id)
            if not test.is_active:
                return Response({'success':False,'message': 'Test is not live'}, status=status.HTTP_400_BAD_REQUEST)
        test = get_object_or_404(Test, id=test_id)
        
        ## if test is being resumed - toh i will send the attempt data in response
        test_attempt = TestAttempt.objects.filter(user=request.user, test=test)
        if test_attempt.exists():
            test_attempt = test_attempt.first()
            test_attempt_serialized = TestAttemptSerializer(test_attempt).data
            return Response({"success":True, "message":"Test resumed successfully", "data":test_attempt_serialized}, status=status.HTTP_200_OK)
        
        ## if test is being started for the first time
        test_attempt = TestAttempt.objects.create(user=request.user, test=test)
        test_attempt_serialized = TestAttemptSerializer(test_attempt).data
        return Response({"success":True, "message":"Test started successfully", "data":test_attempt_serialized}, status=status.HTTP_200_OK)

def calculate_test_attempt_score(test_attempt):
    # test_attempt = TestAttempt.objects.get(id=id)
    print(test_attempt)
    
    score = 0
    for test_question_attempt in test_attempt.question_attempts.all():
        # print(test_question_attempt)
        if (test_question_attempt.status == "Attempted" or test_question_attempt.status == "SaveMarked") and test_question_attempt.is_correct:
            score = score + test_question_attempt.test_question.positive_marks
        elif (test_question_attempt.status == "Attempted" or test_question_attempt.status == "SaveMarked") and not test_question_attempt.is_correct:
            score = score - test_question_attempt.test_question.negative_marks
        else :
            pass
        test_attempt.score = score
        test_attempt.save()
    return score
    
class SubmitTest(APIView):
    permission_classes = [IsAuthenticated, IsPaymentDone]

    def post(self, request, test_id, format=None):
        
        # # check if the data is in correct format & I have all the required fields : test_id
        # # check if the test is live
        # # check if the test is already attempted (if not, save attempt)
        # go to each section and each question and perform the following operations : evaluate correctness, save attempt, foreign key to test_attempt
        # return the test_attempt data in response

        serializer = TestSubmissionSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # (+) I also want to check if the number of questions attempted is equal to the number of questions in the test
        
        if LiveTest.objects.filter(id=test_id).exists():
            test = LiveTest.objects.get(id=test_id)
            if not test.is_active:
                return Response({"success":False, "message":"Test is not live."}, status=status.HTTP_400_BAD_REQUEST)
            # edge case if the live test was over before the user submitted ? tb ky krega ??
        test = get_object_or_404(Test, id=test_id)

        # BT dedo - if test already attempted (and submitted)
        if TestAttempt.objects.filter(user=request.user, test=test).exists():
            test_attempt = TestAttempt.objects.get(user=request.user, test=test)        # I am not using get_or_create because i dont want to return error if attempt exists
            if test_attempt.is_submitted:
                return Response({"success":False, "message":"Test already submitted."}, status=status.HTTP_400_BAD_REQUEST)
        else :
            # test_attempt = TestAttempt.objects.create(user=request.user, test=test)
            return Response({"success":False, "message":"Test not started."}, status=status.HTTP_400_BAD_REQUEST)
        print(test_attempt)

        bad_section_ids = []
        bad_question_ids = []

        # iterate over sections
        for section_data in request.data.get('sections', []):

            section = TestSection.objects.filter(test=test, id=section_data.get('id'))
            if not section.exists():
                bad_section_ids.append(section_data.get('id'))
                continue
            section = section.first()

            # iterate over questions 
            for question_data in section_data["questions"]:
                
                test_question = TestQuestion.objects.filter(section=section, id=question_data.get('test_question'))
                if not test_question.exists():
                    bad_question_ids.append(question_data.get('id'))
                    continue
                test_question = test_question.first()

                # Evaluate if the answer is correct based on the selected option
                try:
                    is_correct = check_answer(test_question.question.id, question_data)          # calls function form questions.utils file
                except Exception as e:
                    print(e)
                    is_correct = False
                    bad_question_ids.append(test_question.id)

                import dateutil.parser
                print(type(question_data["time_taken"]))
                print(dateutil.parser.parse(question_data["time_taken"]))
                # Update the attempt with the user's selected option, status, and correctness
                question_attempt = TestQuestionAttempt.objects.create(
                    test_attempt=test_attempt,
                    test_question=test_question,
                    status=question_data["status"],
                    # time_taken=question_data["time_taken"],
                    is_correct=is_correct
                )
                question_attempt.save()

        print(bad_section_ids) 
        print(bad_question_ids)

        test_attempt.is_submitted = True
        test_attempt.score = calculate_test_attempt_score(test_attempt)
        test_attempt.submission_time = timezone.now()
        test_attempt.save()
        test_attempt_serialized = TestAttemptSerializerFull(test_attempt)
    
        return Response({"success":True, "message":"Test submitted successfully", "data":test_attempt_serialized.data}, status=status.HTTP_200_OK)


class MyResults(APIView):
    permission_classes = [IsAuthenticated, IsPaymentDone]

    def get(self, request, test_id, format=None):
        test = get_object_or_404(Test, id=test_id)
        test_attempt = TestAttempt.objects.filter(user=request.user, test=test)
        if not test_attempt.exists():
            return Response({"success":False,'message': 'Test not started'}, status=status.HTTP_400_BAD_REQUEST)
        
        test_attempt = test_attempt.first()
        test_attempt_serialized = TestAttemptSerializerFull(test_attempt).data
        return Response({"success":True, "message":"Test Result fetched succcessfully", "data":test_attempt_serialized}, status=status.HTTP_200_OK)