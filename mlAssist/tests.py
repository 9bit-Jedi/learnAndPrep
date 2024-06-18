from django.test import TestCase
from jupyter_files.mlassist import main
from django.conf import settings
# from settings import BASE_DIR

MEDIA_DIR = f"{settings.BASE_DIR}\media"

# Create your tests here.
file_path_paper="\mlAssist\paper\paper1.pdf"
file_path_results="\mlAssist\paper\paper1_results.csv"

main(MEDIA_DIR+file_path_paper, MEDIA_DIR+file_path_results)