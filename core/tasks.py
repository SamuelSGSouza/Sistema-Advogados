from celery import shared_task
from time import sleep
from RPA.fase_1.pdf_extractor import main_extrator


@shared_task
def processa_fase_1(files):
    main_extrator(files)

    
