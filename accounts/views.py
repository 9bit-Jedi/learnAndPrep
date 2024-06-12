from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from accounts.serializers import StudentClassSelectionSerializer, UserRegestrationSerializer,UserLoginSerializer,UserProfileSerializer,UserChangePasswordSerializer,SendPasswordResetEmailSerializer , UserPasswordResetSerializer 
from django.contrib.auth import authenticate ,login
from accounts.renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from accounts.models import User
# Create your views here.

# generate token manully 
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
# end of functiion

# register user function 
class UserRegestrationView(APIView):
    renderer_classes = [UserRenderer]
    def post(self, request , formate =None):
        serializer= UserRegestrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            token = get_tokens_for_user(user)
            return Response({'token' : token , 'msg': 'registration successfull'} , status=status.HTTP_201_CREATED)
        return Response({'msg':'regestration unsuccessfull'} , status=status.HTTP_400_BAD_REQUEST)
# end of register user function

class UserLoginView(APIView):
    renderer_classes = [UserRenderer]
    
    def post(self, request , formate = None):
        
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception= True):
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            user = authenticate(email = email , password = password )
            if user is not None:
                token = get_tokens_for_user(user)
                return Response({'token' : token ,'msg' : 'Login successfull'},status=status.HTTP_200_OK)
            else:
                return Response({'errors' : {'non_field_errors' : ['email or Password is not valid']}} ,status=status.HTTP_404_NOT_FOUND)
            
        return Response(serializer.errors , status= status.HTTP_400_BAD_REQUEST)


class UserProfileView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def get(self, request , formate = None):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data , status= status.HTTP_200_OK)
    

class UserChangePasswordView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def post(self, request , formate = None):
        serializer = UserChangePasswordSerializer(data= request.data , context = {'user' : request.user})
        if serializer.is_valid(raise_exception=True):
            return  Response({'msg' : 'password changed successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors , status= status.HTTP_400_BAD_REQUEST)


class SendPasswordResetEmailView(APIView):
    renderer_classes = [UserRenderer]
    def post(self , request , formate = None):
        serializer = SendPasswordResetEmailSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return  Response({'msg' : 'password reset link is sent to your email please check your email'}, status=status.HTTP_200_OK)
        return  Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class  UserPasswordResetView(APIView):
    renderer_classes = [ UserRenderer]
    def post(self , request , uid, token ,formate = None):
        serializer = UserPasswordResetSerializer(data=request.data, context={'uid':uid, 'token':token})
        serializer.is_valid(raise_exception=True)
        return Response({'msg':'Password Reset Successfully'}, status=status.HTTP_200_OK)

class StudentClassSelectionView (APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def post(self, request , formate = None):
        serializer = StudentClassSelectionSerializer(data=request.data, instance=request.user)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'msg': 'Class selection updated successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
