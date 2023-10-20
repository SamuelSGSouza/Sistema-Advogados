from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, View
from django.contrib import messages

from RPA.fase_1.pdf_extractor import main_extrator
from configs import models
from . import models as core_models
from core import tasks
import os

#View inicial do sistema
class DashBoard(TemplateView):
    template_name = "core/dashboard.html"
    def get(self, *args, **kwargs):
        context = {
            'emails_cadastrados': 0,
            'emails_clientes': 0,
            'emails_negativos': 0,
            'dados_finais': 0,
            "processos_cadastrados": core_models.Processo.objects.all().count(),
        }
        try:
            del self.request.session['cadastrando']
        except:
            pass
        return render(self.request, self.template_name, context)

#view da Fase 1
class Fase1(TemplateView):
    template_name = "core/executar_fase1.html"

    def post(self,*args, **kwargs):
        #pegando os arquivos pdfs enviados
        arquivos = self.request.FILES.getlist('arquivos')

        #limpando a pasta RPA/fase_1
        folder = 'RPA/fase_1'
        for file in os.listdir(folder):
            #tirando todos os pdfs
            if file.endswith(".pdf"):
                os.remove(os.path.join(folder, file))

        #salvando os arquivos na pasta RPA/fase_1
        files = []
        for arquivo in arquivos:
            file = 'RPA/fase_1/'+arquivo.name 
            with open(file, 'wb+') as destination:
                for chunk in arquivo.chunks():
                    destination.write(chunk)
            files.append(file)

        # main_extrator(files)
        tasks.processa_fase_1.delay(files)

        messages.success(self.request, 'Processo iniciado com sucesso!')
        return redirect('fase1')

def cadastrar_termos(request):
    with open("Configuracoes/termos_contabilidade.txt", "r") as arquivo:
        termos = arquivo.read()
    termos = termos.split('\n')
    termos = [termo for termo in termos if len(termo) > 4]
    termos = list(set(termos))
    termos = [termo.lower().strip() for termo in termos]

    termos_cadastrar = []
    for termo in termos:
        termos_cadastrar.append(
            models.TermoCategoria(
                termo=termo,
                categoria='Contabilidade',
                fase='Fase 1'
            )
        )
    models.TermoCategoria.objects.bulk_create(termos_cadastrar)

    with open("Configuracoes/termos_engenharia.txt", "r") as arquivo:
        termos = arquivo.read()
    termos = termos.split('\n')
    termos = [termo for termo in termos if len(termo) > 4]
    termos = list(set(termos))
    termos = [termo.lower().strip() for termo in termos]

    termos_cadastrar = []
    for termo in termos:
        termos_cadastrar.append(
            models.TermoCategoria(
                termo=termo,
                categoria='Engenharia',
                fase='Fase 1'
            )
        )
    models.TermoCategoria.objects.bulk_create(termos_cadastrar)

    with open("Configuracoes/termos_grafotecnica.txt", "r") as arquivo:
        termos = arquivo.read()
    termos = termos.split('\n')
    termos = [termo for termo in termos if len(termo) > 4]
    termos = list(set(termos))
    termos = [termo.lower().strip() for termo in termos]

    termos_cadastrar = []
    for termo in termos:
        termos_cadastrar.append(
            models.TermoCategoria(
                termo=termo,
                categoria='Grafotécnica',
                fase='Fase 1'
            )
        )
    models.TermoCategoria.objects.bulk_create(termos_cadastrar)

    return redirect('index')

def cadastrar_termos_negativos(request):
    with open("Configuracoes/negative_keywords.txt", "r") as arquivo:
        termos = arquivo.read()
    termos = termos.split('\n')
    termos = [termo for termo in termos if len(termo) > 4]
    termos = list(set(termos))
    termos = [termo.lower().strip() for termo in termos]

    termos_cadastrar = []
    for termo in termos:
        termos_cadastrar.append(
            models.TermoNegativo(
                termo=termo,
                fase='Fase 1'
            )
        )
    models.TermoNegativo.objects.bulk_create(termos_cadastrar)

    return redirect('index')