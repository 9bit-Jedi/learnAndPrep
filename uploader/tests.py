from questions.models import *
from questions.serializers import *

from accounts.models import User
# from django.conf import settings
# User = settings.AUTH_USER_MODEL
from django.db import transaction
from django.core.files.images import ImageFile

question_id = 'MA02001'

subject_id = Subject.objects.get(id=question_id[0:2])
chapter_id = Chapter.objects.get(id=question_id[0:4])
creator = User.objects.get(name='utsah')
question_url = 'media/questions/Chemistry/Alcohol Ether/question_1.png'

batch = [
  {
    'id': 'MA02001',
    'chapter_id':chapter_id,
    'type':'SMCQ',
    'source':'MODULE',
    'question':ImageFile(open(question_url, 'rb')),
    'creator':creator.pk
  },
  {
    'id':'MA02001',
    'chapter_id':chapter_id.pk,
    'type':'INT',
    'source':'ADV',
    'question':ImageFile(open(question_url, 'rb')),
    'creator':creator.pk
  },
]

serializer_batch = []

for data in batch:
  serializer = QuestionSerializer(data=data) 
  if serializer.is_valid():
    serializer_batch.append(Question(**serializer.validated_data))
    
print(serializer_batch)

# bulk create all instances
with transaction.atomic():
  Chapter.objects.bulk_create(serializer_batch)



Question.objects.create(
  id= question_id,
  chapter_id= chapter_id,
  type= 'MMCQ',
  source= 'ADV',
  question= ImageFile(open(question_url, 'rb')),
  creator= creator
)