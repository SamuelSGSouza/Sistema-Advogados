from celery import shared_task
from time import sleep
from RPA.fase_1.pdf_extractor import main_extrator
from RPA.fase_2.download_pdfs import wrap_downloads
from configs import models


@shared_task
def processa_fase_1(files):
    sleep(3)
    status = models.StatusFase.objects.filter(fase="Fase 1").first()
    status.status = "Processando"
    status.save()

    main_extrator(files)
    status.status = "Finalizado"
    status.save()

@shared_task
def processa_fase_2():
    sleep(3)
    status = models.StatusFase.objects.filter(fase="Fase 2").first()
    status.status = "Processando"
    status.save()

    wrap_downloads()

    status.status = "Finalizado"
    status.save()
    
