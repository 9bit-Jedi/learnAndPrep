from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import generics, status

# Create your views here.
def index(request):
    return HttpResponse("This will be auth api endpoint")