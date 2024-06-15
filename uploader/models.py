from pathlib import Path
from django.db import models

# Create your models here.

class File(models.Model):
  file = models.FileField(upload_to="temp/")
  uploaded_at = models.DateTimeField(auto_now_add=True)
  
  def __str__(self):
    return Path(self.file.name).name
  
  class Meta:
    verbose_name_plural = 'MyFiles'
  
# class Files(models.Model):
#     pdf = models.FileField(upload_to='store/pdfS/')
#     title = models.CharField(max_length=200)
#     def __str__(self) -> str:
#         return self.title

class Img(models.Model):
  file = models.FileField(upload_to="temp/img/")
  uploaded_at = models.DateTimeField(auto_now_add=True)
  
  def __str__(self):
    return Path(self.file.name).name
  
  class Meta:
    verbose_name_plural = 'MyImgs'
  