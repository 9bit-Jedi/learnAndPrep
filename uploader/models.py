from pathlib import Path
from django.db import models

# Create your models here.

class File(models.Model):
  file = models.FileField(upload_to="uploader/files")
  uploaded_at = models.DateTimeField(auto_now_add=True)
  
  # def __str__(self):
  #   return Path(self.file.name).name
  
  class Meta:
    verbose_name_plural = 'MyFiles'
  
class Img(models.Model):
  file = models.FileField(upload_to="uploader/img")
  uploaded_at = models.DateTimeField(auto_now_add=True)
  
  def __str__(self):
    return Path(self.file.name).name
  
  class Meta:
    verbose_name_plural = 'MyImgs'
  