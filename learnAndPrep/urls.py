"""
URL configuration for learnAndPrep project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


# from rest_framework_simplejwt.views import (
#     TokenObtainPairView,
#     TokenRefreshView,
# )

urlpatterns = [
    
    path('api/admin/', admin.site.urls),
    path('api/user/' , include('accounts.urls')),
    path('api/mentorship/' , include('mentorship.urls')),
    
    path('api/questions/', include('questions.urls')),
    path('api/notes/', include('notes.urls')),
    path('api/answer/', include('quiz.urls')),
    
    path('api/mocktest/', include('mockTest.urls')),
    # path('dpp/', include('mlAssist.urls')),
    
    path('api/contact/', include('contactUs.urls')),
    path('api/payments/', include('payments.urls')),
    
    path('api/upload/', include('uploader.urls')), 
    # path("__debug__/", include("debug_toolbar.urls")),
] +static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
