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
    permission_classes = [IsAuthenticated, IsPaymentDone]  # Uncomment to require authentication

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