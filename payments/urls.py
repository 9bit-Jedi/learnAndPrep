from django.urls import path
from .views import CreateOrderView

urlpatterns = [
    # path("<pdf_url>", GetNotes.as_view(), name="get notes pdf file view"),
    # add option in uploader app to upload notes | take care of .pdf extension validation 
    path("create-order/", CreateOrderView.as_view(), name="create_order"),
]