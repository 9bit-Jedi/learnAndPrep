from django.urls import path
from .views import *
urlpatterns = [
    path('get-mentor', getMentorView.as_view(), name='get-mentor'),
    # list of all mentors
    # list of all mentees (meaning have taken mentopship)
    # List of all enrolled students (paid 5k)
    # list of all students onboard (all)
]