from celery import shared_task
from time import sleep
from RPA.fase_1.pdf_extractor import main_extrator
from RPA.fase_2.download_pdfs import wrap_downloads
from RPA.fase_3.fase_3 import main_fase_3
from configs import models
#importando traceback para pegar o erro
import traceback


@shared_task
def processa_fase_1(files):
    status = models.StatusFase.objects.filter(fase="Fase 1").first()
    status.status = "Processando"
    try:
        sleep(3)
        
        status.save()

        main_extrator(files)
        status.status = "Finalizado"
        status.save()
    except Exception as e:
        print(e)
        status.status = "Erro na execução"
        status.save()

@shared_task
def processa_fase_2():
    status = models.StatusFase.objects.filter(fase="Fase 2").first()
    status.status = "Processando"
    try:
        sleep(3)
        
        status.save()

        wrap_downloads()

        status.status = "Finalizado"
        status.save()
    except Exception as e:
        print(e)
        status.status = "Erro na execução"
        status.save()
    
@shared_task
def processa_fase_3():
    status = models.StatusFase.objects.filter(fase="Fase 3").first()
    status.status = "Processando"
    try:
        sleep(3)
        
        status.save()

        main_fase_3()

        status.status = "Finalizado"
        status.save()
    except Exception as e:
        #printando erro completo
        print(traceback.format_exc())
        status.status = "Erro na execução"
        status.save()

@shared_task
def processa_todas_fases(files):
    sleep(3)
    status1 = models.StatusFase.objects.filter(fase="Fase 1").first()
    status1.status = "Processando"
    status1.save()

    status2 = models.StatusFase.objects.filter(fase="Fase 2").first()
    status2.status = "Processando"
    status2.save()

    status3 = models.StatusFase.objects.filter(fase="Fase 3").first()
    status3.status = "Processando"
    status3.save()

    main_extrator(files)
    status1.status = "Finalizado"
    status1.save()

    wrap_downloads()
    status2.status = "Finalizado"
    status2.save()

    main_fase_3()
    status3.status = "Finalizado"
    status3.save()

