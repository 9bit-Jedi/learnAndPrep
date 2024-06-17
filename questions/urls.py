from django.urls import path
from .views import GetQuestionAll, GetQuestion, GetQuestionAllSrc, GetQuestionSrcChapter
from .views import ChapterList_Subject, ViewQuestionImage, ViewExplanationImage, ViewIcon
from quiz.views import GetAnswer

urlpatterns = [
    # path("chapters/", FetchChapters.as_view(), name="All Chapters"),
    path("list-chapters/<subject_id>", ChapterList_Subject.as_view(), name="list chapters using queryparam subject_name = subject"),
    path("all", GetQuestionAll.as_view(), name="question"),
    path("id/<question_id>", GetQuestion.as_view(), name="get question by id"),
    
    path("answer/<question_id>", GetAnswer.as_view(), name="get answer by question id"),
    # path("submit/<question_id>", Submit.as_view(), name="submit solution with query param as question 'type' "),
    
    path("media/questions/<image_name>", ViewQuestionImage.as_view(), name="render any image from qestions"),
    path("media/explanations/<image_name>", ViewExplanationImage.as_view(), name="render any image from qestions"),
    path("media/img/icons/<image_name>", ViewIcon.as_view(), name="render any image from qestions"),
    
    # path("solution/<question_id>", GetSolution.as_view(), name="get question by id"),

    path("<src>/", GetQuestionAllSrc.as_view(), name="questions from a source"),
    path("<src>/<chapter_id>", GetQuestionSrcChapter.as_view(), name="questions from a source and chapter"),

]