from django.contrib import admin
from .models import *

# Register your models here.
class SmcqAdmin(admin.StackedInline):
  model = AnswerSmcq
class MmcqAdmin(admin.StackedInline):
  model = AnswerMmcq
class IntegerTypeAdmin(admin.StackedInline):
  model = AnswerIntegerType
class QuestionAdmin(admin.ModelAdmin):
  inlines = [SmcqAdmin, MmcqAdmin, IntegerTypeAdmin]
  

# admin.site.register(Subject)
# admin.site.register(Chapter)
# admin.site.register(Icon)

admin.site.register(Question)
admin.site.register(AnswerIntegerType)
admin.site.register(AnswerMmcq)
admin.site.register(AnswerSmcq)
admin.site.register(AnswerSubjective)