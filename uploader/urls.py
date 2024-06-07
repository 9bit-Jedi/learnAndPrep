from django.urls import path
from .views import FileUploadView, ImportSubject

urlpatterns = [
    path("csv/", FileUploadView.as_view(), name="file uploader view"),
    path("execute/", ImportSubject, name="file uploader view"),
]