from django.http import HttpResponse
from django.db import IntegrityError 
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
# from rest_framework.decorators import parser_classes
from rest_framework.parsers import FormParser, MultiPartParser

from accounts.models import User
from .serializers import UserSerializer
from accounts.permissions import IsPaymentDone, IsMentorAlloted
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser

from .models import Mentor, Mentee, MentorMenteeRelationship
from .serializers import MentorSerializer, MenteeSerializer, MentorSerializer2, MentorMenteeRelationshipSerializer, AllotedMentorRelationshipSerializer, AllotmentsListSerializer

class UserListView(APIView):
    permission_classes=[IsAdminUser]
    def get(self, *args, **kwargs):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True) 
        return Response(serializer.data, status=status.HTTP_200_OK)

class MenteeListView(APIView):
    permission_classes=[IsAdminUser]
    def get(self, *args, **kwargs):
        users = Mentee.objects.all()
        serializer = MenteeSerializer(users, many=True) 
        return Response(serializer.data, status=status.HTTP_200_OK)

class MentorListView2(APIView):
    permission_classes=[IsAdminUser]
    def get(self, *args, **kwargs):
        users = Mentor.objects.all().order_by('-bandwidth')
        serializer = MentorSerializer2(users, many=True) 
        return Response(serializer.data, status=status.HTTP_200_OK)

class AllotmentsListView(APIView):
    permission_classes=[IsAdminUser]
    def get(self, *args, **kwargs):
        users = MentorMenteeRelationship.objects.all()
        serializer = AllotmentsListSerializer(users, many=True) 
        return Response(serializer.data, status=status.HTTP_200_OK)