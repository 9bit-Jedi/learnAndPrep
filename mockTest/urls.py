from django.urls import path
# from .views import StartTest, SubmitTest, MyResults, TestList
from .views import AvailableTestsList

urlpatterns = [
    # path("start-test/", StartTest.as_view(), name="post request to start test, returns test and question data, qpm - test_id"),
    # path("submit-test/", SubmitTest.as_view(), name="post request to start test, returns test and question data"),
    # path("my-results/", MyResults.as_view(), name="post request to start test, returns test and question data"),
    path('list/', AvailableTestsList.as_view(), name='available-tests-list'),
    # path('tests/<uuid:test_id>/instructions/', TestInstructionsDetail.as_view(), name='test-instructions-detail'),
]