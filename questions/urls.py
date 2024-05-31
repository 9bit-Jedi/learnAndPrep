from django.urls import path
from .views import GetSmcq, GetMmcq, GetIntegerType, GetSmcqAll, GetMmcqAll, GetIntegerTypeAll
from .views import TopicList_Subject, TopicList_Chapter

urlpatterns = [
    # path("chapters/", FetchChapters.as_view(), name="All Chapters"),
    path("smcq/<int:question_id>", GetSmcq, name="smcq"),
    path("mmcq/<int:question_id>", GetMmcq, name="mmcq"),
    path("intg/<int:question_id>", GetIntegerType, name="integer type"),
    path("smcq", GetSmcqAll.as_view(), name="smcq all"),
    path("mmcq", GetMmcqAll.as_view(), name="mmcq all"),
    path("intg", GetIntegerTypeAll.as_view(), name="intg all"),
    
    path("list-topics-from-subject", TopicList_Subject.as_view(), name="list topics using queryparam subject_name = subject"),
    path("list-topics-from-chapter", TopicList_Chapter.as_view(), name="list topics using chapter"),
    
]