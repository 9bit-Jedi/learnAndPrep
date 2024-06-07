from .models import File
from questions.models import Subject, Chapter
from questions.serializers import ChapterSerializer
from django.db import transaction

Subject.objects.create(id = 'MN',subject_name = 'test subject')
# Chapter.objects.create(id = 'MA01',chapter_name = 'test chapter', subject_id = query_MA)

query_PH = Subject.objects.get( id = 'PH' )
query_CH = Subject.objects.get( id = 'CH' )
query_MA = Subject.objects.get( id = 'MA' )


chapter_data = {
  'id': 'MA01',
  'chapter_name': 'testtt',
  'subject_id': query_MA
}

Chapter.objects.create(chapter_data)

serializer = ChapterSerializer(data=chapter_data)
if serializer.is_valid():
  serializer.save()


with transaction.atomic():
  Chapter.objects.bulk_create(serializer)
  
# type checking
print(query_CH.id, query_MA.id, query_PH)
print(type(query_CH.id))

