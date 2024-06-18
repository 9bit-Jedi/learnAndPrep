from django.shortcuts import render
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from rest_framework import status
import pandas as pd
from .models import PaperPdf, ResultsPdf, DppPdf

from mlAssist.jupyter_files.mlassist import main


class PdfUploadView(APIView):
  parser_classes = [MultiPartParser, FormParser]

  def post(self, request, format=None):    
    paper_pdf = request.data['paper_pdf']
    results_pdf = request.data['results_pdf']
    
    paper_obj = PaperPdf.objects.create(file=paper_pdf)
    results_obj = ResultsPdf.objects.create(file=results_pdf)
    # return ImportPaper(obj.file.path)
    
    return call_model(paper_obj.file.path, results_obj.file.path)
  
    # if(request.data['contentType']=='paper'):
    #   obj = PaperPdf.objects.create(file=file)
    #   return ImportPaper(obj.file.path)
    # return None

# from jupyter_files.mlassist import main

def call_model(file_path_paper, file_path_results):
  # call model here with 'file_path's
  return main(file_path_paper, file_path_results)
  return None

