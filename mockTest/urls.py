from django.urls import path
# from .views import StartTest, SubmitTest, MyResults, TestList
from .views import AvailableTestsList, MyResults, StartTest, SubmitTest

urlpatterns = [
    path("start-test/<test_id>", StartTest.as_view(), name="post request to start test, returns test and question data, qpm - test_id"),
    path("submit-test/<test_id>", SubmitTest.as_view(), name="post request to start test, returns test and question data"),
    path("my-results/<test_id>", MyResults.as_view(), name="post request to start test, returns test and question data"),
    path('list/', AvailableTestsList.as_view(), name='available-tests-list'),
    # path('tests/<uuid:test_id>/instructions/', TestInstructionsDetail.as_view(), name='test-instructions-detail'),
]