from django.urls import path
from .views import GetQuestionAll, GetQuestion, GetQuestionChapter, GetAnswer, GetQuestionAllSrc
from .views import ChapterList_Subject, ViewImage

urlpatterns = [
    # path("chapters/", FetchChapters.as_view(), name="All Chapters"),
    path("list-chapters/<subject_id>", ChapterList_Subject.as_view(), name="list chapters using queryparam subject_name = subject"),
    path("all", GetQuestionAll.as_view(), name="question"),
    path("<src>", GetQuestionAllSrc.as_view(), name="questions from a source"),
    path("id/<question_id>", GetQuestion.as_view(), name="get question by id"),
    # path("", GetQuestionChapter.as_view(), name="get question by id, query_param : question_id"),
    # path("answer", GetAnswer.as_view(), name="get answer by question id, query_param : question_id"),
    path("images/<image_name>", ViewImage.as_view(), name="list topics using chapter"),



    # path("answer/<int:question_id>", GetQuestion.as_view(), name="question"),
    # path("mmcq/<int:question_id>", GetMmcq, name="mmcq"),
    # path("intg/<int:question_id>", GetIntegerType, name="integer type"),
    # path("smcq", GetSmcqAll.as_view(), name="smcq all"),
    # path("mmcq", GetMmcqAll.as_view(), name="mmcq all"),
    # path("intg", GetIntegerTypeAll.as_view(), name="intg all"), 
    
    # path("list-topics-from-chapter", TopicList_Chapter.as_view(), name="list topics using chapter"),
    
    
    # list smcq & mmcq & integ type by label query param 
]