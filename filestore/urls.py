from django.contrib import admin
from django.urls import path , include
from rest_framework.routers import DefaultRouter
from .views import FileViewSets

router = DefaultRouter()
router.register('files' , FileViewSets , basename='files')


urlpatterns = [
    path('pdf/' , include(router.urls)),
]