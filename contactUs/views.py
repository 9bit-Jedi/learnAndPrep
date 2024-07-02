from django.shortcuts import render

# Create your views here.
from django.views import View
from django.http import HttpResponse  # Import Response class
from .models import ContactUs
from accounts.utils import Util

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .serializers import ContactUsSerializer

class ContactusView(APIView):
  permission_classes = [AllowAny]

  def post(self, request):
    print(request.data)
    serializer = ContactUsSerializer(data=request.data)
    if serializer.is_valid():
      name = serializer.validated_data['name']
      email = serializer.validated_data['email']
      mobile_no = serializer.validated_data['mobile_no']
      subject = serializer.validated_data['subject']
      message = serializer.validated_data['message']
      contact = ContactUs(name=name, email=email, mobile_no=mobile_no, subject=subject, message=message)
      contact.save()
      
      # Send OTP to the user's email
      team_email_data = {
          'subject': f"Support Request - {subject}",
          'body': f"Hello Team,\n\nA new contact request has been received. Here are the details:\n\nName: {name}\nEmail: {email}\nMobile Number: {mobile_no}\nSubject: {subject}\nMessage: {message}\n\nPlease review and take the necessary action.\n\nBest,\nYour Automated System",
          'to_email': 'utsah470@gmail.com'
      }
      email_data = {
          'subject': f"Thank you for contacting us, {name}!",
          'body': f"Dear {name},\n\nThank you for reaching out to us. We have received your message regarding '{subject}'. Our team will review your inquiry and get back to you as soon as possible.\n\nHere is a summary of your message:\nName: {name}\nEmail: {email}\nMobile Number: {mobile_no}\nSubject: {subject}\nMessage: {message}\n\nThank you for contacting us.\n\nBest Regards,\nSupport Team VJ Sir",
          'to_email': email
      }
      
      try:
          Util.send_mail(team_email_data)
          Util.send_mail(email_data)
          return Response({'msg': 'Email has been sent to your email address.'}, status=status.HTTP_200_OK)
      except Exception as e:
          print(e)     
      
      return Response("There was an error sending the email. Try again in sometime.", status=status.HTTP_400_BAD_REQUEST)
    else:
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)