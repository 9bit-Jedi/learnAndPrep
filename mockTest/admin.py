from django.contrib import admin
from .models import *

# Register your models here. 

# admin.site.register(Instructions)
admin.site.register(TestSeries)
admin.site.register(LiveTest)
admin.site.register(Test)
admin.site.register(CustomTest)
admin.site.register(TestSection)
admin.site.register(TestQuestion)
admin.site.register(TestAttempt)
admin.site.register(TestQuestionAttempt)