from django.contrib.contenttypes.models import ContentType
from django.db import connection

def run():
  content_types = ContentType.objects.all()
  print(content_types)

run()