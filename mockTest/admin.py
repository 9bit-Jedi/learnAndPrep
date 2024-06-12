from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(LiveTest)
admin.site.register(Test)
admin.site.register(TestAttempt)
admin.site.register(TestQuestion)