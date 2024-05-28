from django.urls import path
from .views import FetchQuestionsAll, FetchChapters, FetchQuestion

urlpatterns = [
    path("all/", FetchQuestionsAll.as_view(), name="index"),
    path("chapters/", FetchChapters.as_view(), name="All Chapters"),
    path("<int:id>", FetchQuestion.as_view(), name="All Chapters"),
]