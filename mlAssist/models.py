from django.db import models
from pathlib import Path

# Create your models here.

class PaperPdf(models.Model):
  file = models.FileField(upload_to="mlAssist/paper/")
  
  def __str__(self):
      return Path(self.file.name).name

class ResultsPdf(models.Model):
  paper_id = models.ForeignKey(PaperPdf, on_delete=models.CASCADE)
  file = models.FileField(upload_to="mlAssist/results/")
  
  def __str__(self):
      return Path(self.file.name).name

class DppPdf(models.Model):
  file = models.FileField(upload_to="mlAssist/dpp-final/")
  
  def __str__(self):
      return Path(self.file.name).name
  