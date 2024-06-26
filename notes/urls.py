from django.urls import path
from .views import GetNotes, ListNotes

urlpatterns = [
    path("chapter/<chapter_id>", ListNotes.as_view(), name="get notes list"),
    path("<pdf_url>", GetNotes.as_view(), name="get notes pdf file view"),
    # add option in uploader app to upload notes | take care of .pdf extension validation 
]