import ast
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate ,login
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from django.http import HttpResponse
from accounts.utils import Util
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.exceptions import TokenError

import random
from datetime import datetime, timedelta
from django.utils import timezone
import phonenumbers


from .models import User, UserOTP, UserMobileNoOTP
from .renderers import UserRenderer
from .serializers import StudentClassSelectionSerializer, UserRegestrationSerializer,UserLoginSerializer,UserProfileSerializer,UserChangePasswordSerializer,SendPasswordResetEmailSerializer , UserPasswordResetSerializer, TokenVerificationSerializer, TokenVerificationSerializer

from .serializers import OTPVerificationSerializer,WebsiteUserRegestrationSerializer
from .serializers import MobileNoOTPVerificationSerializer, MobileNoOTPSendSerializer
from .models import UserOTP
from .models import UserOTP

User = get_user_model()
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
    # permission_classes = [AllowAny]

    def post(self, request , formate =None):
        serializer= UserRegestrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.validated_data['email']
            
            # Generate OTP
            # Generate OTP with creation time
            otp, otp_created_at = Util.generate_otp()
            
            # Store OTP and creation time in session
            request.session['temp_user_data'] = serializer.validated_data
            request.session['otp'] = otp
            request.session['otp_created_at'] = otp_created_at  # Store OTP creation time

            # Send OTP to the user's email
            email_data = {
                'subject': 'Your OTP for Registration',
                'body': f'Your OTP for registration is {otp}. Please enter this code to complete your registration.',
                'to_email': email
            }
            try:
                Util.send_otp_mail(email_data)
                # print(otp, email)
                return Response({'msg': 'OTP sent to your email. Please verify to complete registration.'}, status=status.HTTP_200_OK)
            except Exception as e:
                print(e)        
         

        
        return Response({'msg': 'Registration unsuccessful'}, status=status.HTTP_400_BAD_REQUEST)
# end of register user function

class UserLoginView(APIView):
    renderer_classes = [UserRenderer]
    # permission_classes = [AllowAny]
    
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

class UserLogoutView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            refresh = request.data["refresh"]

            # Blacklist the access token
            refresh_token_obj = RefreshToken(refresh)
            refresh_token_obj.blacklist()

            return Response({"msg": "Logout successful"}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class UserProfileView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated] 

    def get(self, request , formate = None):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data , status= status.HTTP_200_OK)

class UserPermissionView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = request.user
        return Response({'is_admin': user.is_admin, 'is_mobile_no_verified': user.is_mobile_no_verified, 'is_payment_done': user.is_payment_done, 'is_mentor_alloted': user.is_mentor_alloted}, status=status.HTTP_200_OK)

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
    # permission_classes = [IsAuthenticated]
    
    def post(self , request , formate = None):
        serializer = SendPasswordResetEmailSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return  Response({'msg' : 'password reset link is sent to your email please check your email'}, status=status.HTTP_200_OK)
        return  Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class  UserPasswordResetView(APIView):
    renderer_classes = [ UserRenderer]
    # permission_classes = [ IsAuthenticated]
    
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
            user = serializer.save()
            selected_class = user.student_class
            return Response({'msg': 'Class selection updated successfully', 'selected_class': selected_class}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class UserUnregisterView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]  
    def delete(self, request, format=None):
        user = request.user
        user.delete()
        return Response({'msg': 'User unregistered successfully'}, status=status.HTTP_200_OK)
    

class VerifyOTPView(APIView):
    
    def post(self, request, format=None):
        # print(request.session['temp_user_data'])
        
        otp = request.data.get('otp')
        # print(otp)
        stored_otp = request.session.get('otp')
        print(otp == stored_otp)
        # print(stored_otp)
        otp_created_at = request.session.get('otp_created_at')
        
        if otp == stored_otp and not Util.is_otp_expired(otp_created_at):
            temp_user_data = request.session.get('temp_user_data')
            if temp_user_data:
                serializer = UserRegestrationSerializer(data=temp_user_data)
                if serializer.is_valid():
                    user = serializer.save()
                    token = get_tokens_for_user(user)
                    # Clean up session data
                    del request.session['temp_user_data']
                    del request.session['otp']
                    del request.session['otp_created_at']
                    return Response({'token': token, 'msg': 'Registration successful'}, status=status.HTTP_201_CREATED)
        
        return Response({'msg': 'Invalid or expired OTP'}, status=status.HTTP_400_BAD_REQUEST)


# DRY principles ki {seedhe maut}
class WebsiteUserRegestrationView(APIView):
    renderer_classes = [UserRenderer]
    # permission_classes = [AllowAny]
    
    def post(self, request , formate =None):
        serializer= WebsiteUserRegestrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            validated_data = serializer.validated_data
            # Generate OTP
            otp = ''.join([str(random.randint(0, 9)) for _ in range(6)])
            # Update validated data with OTP and save user (exclude password2)
            # validated_data.pop('password2')
            # temp_user_data = serializer.validated_data.pop('password2')
            # print(type(serializer.validated_data.pop('password2')))
            
            try:
                UserOTP.objects.filter(email=validated_data['email']).delete() #clear previous otps
            except UserOTP.DoesNotExist:
                pass 

            # Create user without OTP fields
            otp_object = UserOTP.objects.create(
                email = validated_data['email'],
                otp = otp,
                otp_created_at = timezone.now(),
                temp_user_data = validated_data,
            )

            otp_object.save()
            # print(otp, validated_data['email'])
            
            email_data = {
                'subject': 'Verification OTP',
                'body': f'Your OTP for registration is: {otp}',
                'to_email': validated_data['email']
            }
            Util.send_otp_mail(email_data)
            
            context = {'msg':'OTP sent to your email. Please verify to complete registration.', 'email':validated_data['email']}
            return  Response(context, status=status.HTTP_201_CREATED)
        
        print(serializer.errors)
        return  Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OTPVerificationView(APIView):
    # permission_classes = [AllowAny]
    def post(self, request):

        email = request.data['params']['email']         
        print(email)
        serializer = OTPVerificationSerializer(data=request.data)

        if serializer.is_valid():
            otp = serializer.validated_data.get('otp')
            # email = serializer.validated_data.get('email')
            
            try:
                user_otp = UserOTP.objects.get(email=email)
                print(user_otp, user_otp.email, user_otp.temp_user_data)
                if user_otp.is_otp_expired(): 
                    return Response({'error': 'OTP expired'}, status=status.HTTP_400_BAD_REQUEST)

                if user_otp.otp == otp:
                    temp_user_data = ast.literal_eval(user_otp.temp_user_data) 
                    # print(type(temp_user_data))
                    serializer = UserRegestrationSerializer(data=temp_user_data)
                    
                    if serializer.is_valid():
                        user = serializer.save()
                        token = get_tokens_for_user(user)
                        user_otp.delete()  
                        
                        return Response({'token': token, 'msg': 'Registration successful'}, status=status.HTTP_201_CREATED)

                return Response({'error': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)
            except UserOTP.DoesNotExist:
                return Response({'error': 'Invalid email or OTP'}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MobileNoOTPSendView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = MobileNoOTPSendSerializer(data=request.data)
        if serializer.is_valid():
            mobile_no = request.data.get('mobile_no')
            # get_object_or_404(User, mobile_no=mobile_no)
            user_identifier = request.user.id
            
            # Generate OTP
            otp, otp_created_at = Util.generate_otp()
            
            otp_object = UserMobileNoOTP.objects.filter(user_identifier=user_identifier)
            otp_object.delete() if otp_object.exists() else None
            
            # Save OTP and user identifier data
            otp_object = UserMobileNoOTP.objects.create(
                user_identifier=user_identifier,
                mobile_no=mobile_no,
                otp=otp,
                otp_created_at = otp_created_at
            )
            otp_object.save()
            print(otp_object.mobile_no, otp_object.otp)
            
            # Send OTP to Facebook API
            response = Util.send_whatsapp_otp(otp, mobile_no=mobile_no)
            # response = Util.send_quick_sms_otp(otp, mobile_no=mobile_no)
            # response = Util.send_dlt_sms_otp(otp, mobile_no=mobile_no)

            if response.status_code == 200:
                return Response({'msg': f"OTP sent to your mobile number {mobile_no}"}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Failed to send OTP'}, status=status.HTTP_400_BAD_REQUEST)
            
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class MobileNoOTPVerificationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):

        mobile_no = request.data['params']['mobile_no']  
        user_identifier = request.user.id   
        # user identifier is user id
        
        print(mobile_no, user_identifier)
        serializer = MobileNoOTPVerificationSerializer(data=request.data)

        if serializer.is_valid():
            otp = serializer.validated_data.get('otp')
            
            try:
                user_mobile_no_otp = get_object_or_404(UserMobileNoOTP, user_identifier=user_identifier, mobile_no=mobile_no)
                # user_mobile_no_otp = UserMobileNoOTP.objects.get(user_identifier=user_identifier, mobile_no=mobile_no)
                print(user_mobile_no_otp, user_mobile_no_otp.mobile_no, user_mobile_no_otp.otp)
                
                if user_mobile_no_otp.is_otp_expired(): 
                    return Response({'error': 'OTP expired'}, status=status.HTTP_400_BAD_REQUEST)
                
                if user_mobile_no_otp.otp == otp:
                    user = get_object_or_404(User, id=user_identifier)
                    print(user)
                    print(user.mobile_no )
                    parsed_number = phonenumbers.parse(user_mobile_no_otp.mobile_no, "IN")
                    user.mobile_no = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.E164).lstrip("0")
                    user.is_mobile_no_verified = True
                    user.save()
                    
                    user_mobile_no_otp.delete()  
                    return Response({'msg': 'Mobile number verified'}, status=status.HTTP_200_OK)

                return Response({'error': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)
            except UserMobileNoOTP.DoesNotExist:
                return Response({'error': 'Invalid phone or OTP'}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VerifyTokenView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        serializer = TokenVerificationSerializer(data=request.data)
        if serializer.is_valid():
            token = serializer.validated_data['token']
            try:
                # Decode the token to ensure it is valid
                AccessToken(token)
                return Response({'valid': True}, status=status.HTTP_200_OK)
            except TokenError:
                print(e)
                return Response({'valid': False, 'msg': 'Invalid or expired token'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class VerifyRefreshTokenView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        serializer = TokenVerificationSerializer(data=request.data)
        if serializer.is_valid():
            token = serializer.validated_data['token']
            try:
                # Decode the token to ensure it is valid
                RefreshToken(token)
                return Response({'valid': True}, status=status.HTTP_200_OK)
            except TokenError:
                return Response({'valid': False, 'msg': 'Invalid or expired token'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)