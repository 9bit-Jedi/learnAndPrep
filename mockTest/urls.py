from django.urls import path
# from .views import StartTest, SubmitTest, MyResults, TestList
from .views import TestList

urlpatterns = [
    # path("start-test/", StartTest.as_view(), name="post request to start test, returns test and question data, qpm - test_id"),
    # path("submit-test/", SubmitTest.as_view(), name="post request to start test, returns test and question data"),
    # path("my-results/", MyResults.as_view(), name="post request to start test, returns test and question data"),
    # path("execute/", ImportSubject, name="file uploader view"),
    path("test-list/", TestList.as_view(), name="test list"),
]