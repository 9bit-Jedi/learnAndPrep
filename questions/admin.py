from django.contrib import admin
from .models import *

# Register your models here.
class SmcqAdmin(admin.StackedInline):
  model = Smcq
class MmcqAdmin(admin.StackedInline):
  model = Mmcq
class IntegerTypeAdmin(admin.StackedInline):
  model = IntegerType
class QuestionAdmin(admin.ModelAdmin):
  inlines = [SmcqAdmin, MmcqAdmin, IntegerTypeAdmin]
  


admin.site.register(Question)
admin.site.register(IntegerType)
admin.site.register(Mmcq)
admin.site.register(Smcq)
admin.site.register(Subject)
admin.site.register(Chapter)
admin.site.register(Topic)
