# from django.http import HttpResponse
# from django.db import IntegrityError 
# from django.shortcuts import get_object_or_404
# from rest_framework import status
# from rest_framework.views import APIView
# from rest_framework.response import Response
# # from rest_framework.decorators import parser_classes
# from rest_framework.parsers import FormParser, MultiPartParser

# from accounts.models import User
# from .serializers import UserSerializer
# from accounts.permissions import IsPaymentDone, IsMentorAlloted
# from rest_framework.permissions import IsAuthenticated, AllowAny

# from .models import Mentor, Mentee, MentorMenteeRelationship
# from .serializers import MentorSerializer, MenteeSerializer, MentorMenteeRelationshipSerializer, AllotedMentorRelationshipSerializer

# class UserListView(APIView):
#     def get(self):
#         users = User.objects.all()
#         serializer = UserSerializer(users)
#         return HttpResponse(serializer.data, status=status.HTTP_200_OK)