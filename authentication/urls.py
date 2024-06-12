
from django.contrib import admin
from django.urls import path , include
from django.conf import settings
from django.conf.urls.static import static
from home.views import *

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/user/' , include('accounts.urls')),
    path('api/storage/' , include('filestore.urls')),
]+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
