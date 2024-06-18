from django.urls import path
from .views import GetQuiz, GetAnswer

urlpatterns = [
    # path("quiz/", GetQuiz.as_view(), name="file uploader view"),
    path("<question_id>", GetAnswer.as_view(), name="GET by question_id & POST by question number and matching request body"),
]