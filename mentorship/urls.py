from django.urls import path
from .views import *
from .views_admin import *

urlpatterns = [
    path('get-mentor', getMentorView.as_view(), name='get-mentor'),
    path('random-mentor', RandomMentorView.as_view(), name='random-mentor'),
    
    path('list-users', UserListView.as_view(), name='list-students'),
    path('list-mentees', MenteeListView.as_view(), name='list-mentee'),
    path('list-mentors', MentorListView2.as_view(), name='list-mentor-with-allotments-only'),
    path('list-allotments', AllotmentsListView.as_view(), name='list-allotments') 
]