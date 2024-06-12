from django.urls import path
from .views import FileUploadView, ImportSubject, ImageUploadView

urlpatterns = [
    path("csv/", FileUploadView.as_view(), name="file uploader view"),
    path("img/", ImageUploadView.as_view(), name="img uploader view"),
    path("execute/", ImportSubject, name="file uploader view"),
]