from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Mentor)
admin.site.register(Mentee) 
admin.site.register(MentorMenteeRelationship)