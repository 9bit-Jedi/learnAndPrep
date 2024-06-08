from django.urls import path ,include
from . import views
from django.contrib import admin

urlpatterns = [
    path("", views.index, name="index"),
    path('admin/', admin.site.urls),
    path('auth/', include('django.contrib.auth.urls')),
    path('__debug__/', include('debug_toolbar.urls')),
]