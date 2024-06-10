from django.urls import path
from .views import GetQuestionAll, GetQuestion, GetAnswer, GetQuestionAllSrc, GetQuestionSrcChapter, Submit
from .views import ChapterList_Subject, ViewImage

urlpatterns = [
    # path("chapters/", FetchChapters.as_view(), name="All Chapters"),
    path("list-chapters/<subject_id>", ChapterList_Subject.as_view(), name="list chapters using queryparam subject_name = subject"),
    path("all", GetQuestionAll.as_view(), name="question"),
    path("id/<question_id>", GetQuestion.as_view(), name="get question by id"),
    
    path("answer/<question_id>", GetAnswer.as_view(), name="get answer by question id"),
    path("submit/<question_id>", Submit.as_view(), name="submit solution with query param as question 'type' "),
    
    path("<src>/", GetQuestionAllSrc.as_view(), name="questions from a source"),
    path("<src>/<chapter_id>", GetQuestionSrcChapter.as_view(), name="questions from a source and chapter"),
    
    # path("solution/<question_id>", GetSolution.as_view(), name="get question by id"),


    path("images/<image_name>", ViewImage.as_view(), name="render any image from qestions"),
]