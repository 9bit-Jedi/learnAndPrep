from django.db import models
# Create your models here.
class Files(models.Model):
    pdf = models.FileField(upload_to='store/pdfS/')
    title = models.CharField(max_length=200)
    def __str__(self) -> str:
        return self.title
