import json
from django.shortcuts import render, get_object_or_404
from django.http import Http404, HttpResponse
from django.core.exceptions import ValidationError
from django.db import IntegrityError 

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status, permissions
from rest_framework.permissions import IsAuthenticated
from accounts.permissions import IsPaymentDone, IsMentorAlloted

from questions.models import Chapter, Question, AnswerIntegerType, AnswerMmcq, AnswerSmcq, AnswerSubjective
from questions.serializers import QuestionSerializer, AnswerMmcqSerializer, AnswerIntegerTypeSerializer, AnswerSmcqSerializer, AnswerSubjectiveSerializer

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
    
class StartTest(APIView):
    permission_classes = [IsAuthenticated, IsPaymentDone]

    def post(self, request, format=None):
        test_id = request.data.get('test_id', None)
        if test_id is None:
            return Response({'error': 'test_id not provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        test = get_object_or_404(Test, id=test_id)
        if LiveTest.objects.filter(id=test_id).exists():
            live_test = LiveTest.objects.get(id=test_id)
            if not live_test.is_active:
                return Response({'error': 'Test is not live'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'Test not found'}, status=status.HTTP_404_NOT_FOUND)
        
        question_attempt = TestAttempt.objects.filter(user=request.user, test=test)
        if question_attempt.exists():
            question_attempt = question_attempt.first()
            question_attempt_serialized = TestAttemptSerializer(question_attempt).data
            return Response(question_attempt_serialized, status=status.HTTP_200_OK)
        
        question_attempt = TestAttempt.objects.create(user=request.user, test=test)
        question_attempt_serialized = TestAttemptSerializer(question_attempt).data
        return Response(question_attempt_serialized, status=status.HTTP_201_CREATED)

class SubmitTest(APIView):
    permission_classes = [IsAuthenticated, IsPaymentDone]

    def post(self, request, format=None):
        test_id = request.data.get('test_id', None)
        if test_id is None:
            return Response({'error': 'test_id not provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        test = get_object_or_404(Test, id=test_id)
        if LiveTest.objects.filter(id=test_id).exists():
            live_test = LiveTest.objects.get(id=test_id)
            if not live_test.is_active:
                return Response({'error': 'Test is not live'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'Test not found'}, status=status.HTTP_404_NOT_FOUND)
        
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