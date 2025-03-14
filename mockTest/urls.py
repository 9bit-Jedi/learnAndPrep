from django.urls import path
# from .views import StartTest, SubmitTest, MyResults, TestList
from .views import AvailableTestSeriesList, TestsFromSeriesList, AvailableTestsList, MyResults, StartTest, SubmitTest, CreateRandomTest

urlpatterns = [
    path('list/', AvailableTestsList.as_view(), name='available-tests-list'),
    # list all series
    path("series/", AvailableTestSeriesList.as_view(), name="available-series-list"),
    # list all test in a series
    path("series/<series_id>/", TestsFromSeriesList.as_view(), name="available-tests-list"),
    
    path("start-test/<test_id>", StartTest.as_view(), name="post request to start test, returns test and question data, qpm - test_id"),
    path("submit-test/<test_id>", SubmitTest.as_view(), name="post request to start test, returns test and question data"),
    path("result/<test_id>", MyResults.as_view(), name="post request to start test, returns test and question data"),
    # path('tests/<uuid:test_id>/instructions/', TestInstructionsDetail.as_view(), name='test-instructions-detail'),

    path("create-random-test/", CreateRandomTest.as_view(), name='create-random-test'),
]   