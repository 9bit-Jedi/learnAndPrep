from django.urls import path
from .views import FetchQuestionsAll

urlpatterns = [
    path("all/", FetchQuestionsAll.as_view(), name="index"),
]