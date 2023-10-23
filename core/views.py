from typing import Any
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, View
from django.contrib import messages

from configs import models
from . import models as core_models
from core import tasks
import os
import pandas as pd

from RPA.fase_3.fase_3 import main_fase_3

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

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        status = models.StatusFase.objects.filter(fase="Fase 1").first()
        if status.status == "Processando":
            messages.warning(self.request, f'Processo iniciado em {status.data_modificado.strftime("%d/%m/%Y")} às {status.data_modificado.strftime("%H:%M:%S")}')
        if status.status == "Finalizado":
            messages.success(self.request, f'Processo finalizado em {status.data_modificado.strftime("%d/%m/%Y")} às {status.data_modificado.strftime("%H:%M:%S")}')
            status.status = "Iniciado"
            status.save()
        context['status'] = status
        return context

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
        models.StatusFase.objects.update_or_create(fase="Fase 1", status="Iniciado")
        tasks.processa_fase_1.delay(files)

        messages.success(self.request, 'Processo iniciado com sucesso! Recarregue a página para atualizar o status.')
        return redirect('fase1')

#view da Fase 2
class Fase2(TemplateView):
    template_name = "core/executar_fase2.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        status = models.StatusFase.objects.filter(fase="Fase 2").first()
        if status.status == "Processando":
            messages.warning(self.request, f'Processo iniciado em {status.data_modificado.strftime("%d/%m/%Y")} às {status.data_modificado.strftime("%H:%M:%S")}')
        if status.status == "Finalizado":
            messages.success(self.request, f'Processo finalizado em {status.data_modificado.strftime("%d/%m/%Y")} às {status.data_modificado.strftime("%H:%M:%S")}')
            status.status = "Iniciado"
            status.save()
        context['status'] = status
        return context

    def post(self,*args, **kwargs):
        models.StatusFase.objects.update_or_create(fase="Fase 2", status="Iniciado")
        tasks.processa_fase_2.delay()

        messages.success(self.request, 'Processo iniciado com sucesso! Recarregue a página para atualizar o status.')
        return redirect('fase2')

class Fase3(TemplateView):
    template_name = "core/executar_fase3.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        status = models.StatusFase.objects.filter(fase="Fase 3").first()
        if status.status == "Processando":
            messages.warning(self.request, f'Processo iniciado em {status.data_modificado.strftime("%d/%m/%Y")} às {status.data_modificado.strftime("%H:%M:%S")}')
        if status.status == "Finalizado":
            messages.success(self.request, f'Processo finalizado em {status.data_modificado.strftime("%d/%m/%Y")} às {status.data_modificado.strftime("%H:%M:%S")}')
            status.status = "Iniciado"
            status.save()
        context['status'] = status
        return context

    def post(self,*args, **kwargs):
        models.StatusFase.objects.update_or_create(fase="Fase 3", status="Iniciado")
        main_fase_3()

        messages.success(self.request, 'Processo iniciado com sucesso! Recarregue a página para atualizar o status.')
        return redirect('fase3')

def cadastrar_sec_desejadas(request):
    models.SecoesDesejadas.objects.all().delete()
    secoes = []
    with open("Configuracoes/tipos_secoes.txt", "r", encoding="utf-8") as f:
        ls = f.read().split("\n")
        for l in ls:
            secoes.append(l.strip())

    secoes_cadastrar = []
    for secao in secoes:
        secoes_cadastrar.append(
            models.SecoesDesejadas(
                secao=secao,
                fase='Fase 2'
            )
        )
    models.SecoesDesejadas.objects.bulk_create(secoes_cadastrar)

    return redirect('index')

def cadastrar_termos(request):
    #excluir todos os termos
    # models.TermoCategoria.objects.all().delete()
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
    models.TermoCategoria.objects.bulk_create(
        termos_cadastrar,
        update_conflicts=True,
        unique_fields=['termo',],
        update_fields=['categoria', 'fase']
        )
    

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
    models.TermoCategoria.objects.bulk_create(termos_cadastrar,update_conflicts=True,
        unique_fields=['termo',],
        update_fields=['categoria', 'fase']
        )

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
    models.TermoCategoria.objects.bulk_create(termos_cadastrar,update_conflicts=True,
        unique_fields=['termo',],
        update_fields=['categoria', 'fase']
        )
    return redirect('index')

def cadastrar_nomes_masculinos(request):
    with open("Configuracoes/nomes_masculinos.txt", "r") as arquivo:
        nomes = arquivo.read()
    nomes = nomes.split('\n')
    nomes = [nome for nome in nomes if len(nome) > 4]
    nomes = list(set(nomes))
    nomes = [nome.lower().strip() for nome in nomes]

    nomes_cadastrar = []
    for nome in nomes:
        nomes_cadastrar.append(
            models.NomesMasculinos(
                nome=nome,
                fase='Fase 3'
            )
        )
    models.NomesMasculinos.objects.bulk_create(nomes_cadastrar)

    return redirect('index')

def termos_remocao_pagina_email(request):
    with open("Configuracoes/termos_remocao_pagina_email.txt", "r") as arquivo:
        termos = arquivo.read()
    termos = termos.split('\n')
    termos = [termo for termo in termos if len(termo) > 4]
    termos = list(set(termos))
    termos = [termo.lower().strip() for termo in termos]

    termos_cadastrar = []
    for termo in termos:
        termos_cadastrar.append(
            models.TermosRemocaoPaginaEmail(
                termo=termo,
                fase='Fase 1'
            )
        )
    models.TermosRemocaoPaginaEmail.objects.bulk_create(termos_cadastrar)

    return redirect('index')

def cadastrar_emails_negativos(request):
    with open("Configuracoes/emails_negativos.txt", "r") as arquivo:
        emails = arquivo.read()
    emails = emails.split('\n')
    emails = [email for email in emails if len(email) > 4]
    emails = list(set(emails))
    emails = [email.lower().strip() for email in emails]

    emails_cadastrar = []
    for email in emails:
        emails_cadastrar.append(
            models.EmailsNegativos(
                email=email,
                fase='Fase 3'
            )
        )
    models.EmailsNegativos.objects.bulk_create(emails_cadastrar)

    return redirect('index')

def cadastrar_termos_email_advogados(request):
    with open("Configuracoes/termos_email_advogado.txt", "r") as arquivo:
        termos = arquivo.read()
    termos = termos.split('\n')
    termos = [termo for termo in termos if len(termo) >= 4]
    termos = list(set(termos))
    termos = [termo.lower().strip() for termo in termos]

    termos_cadastrar = []
    for termo in termos:
        termos_cadastrar.append(
            models.TermosEmailAdvogados(
                termo=termo,
                fase='Fase 3'
            )
        )
    models.TermosEmailAdvogados.objects.bulk_create(termos_cadastrar)

    return redirect('index')

def cadastrar_termos_negativos_nome_advogado(request):
    with open("Configuracoes/termos_negativos_nome_advogado.txt", "r") as arquivo:
        termos = arquivo.read()
    termos = termos.split('\n')
    termos = [termo for termo in termos if len(termo) > 4]
    termos = list(set(termos))
    termos = [termo.lower().strip() for termo in termos]

    termos_cadastrar = []
    for termo in termos:
        termos_cadastrar.append(
            models.TermoNegativoNomeAdvogado(
                termo=termo,
                fase='Fase 3'
            )
        )
    models.TermoNegativoNomeAdvogado.objects.bulk_create(termos_cadastrar)

    return redirect('index')

def cadastrar_emails_clientes(request):
    with open("Configuracoes/emails_clientes.txt", "r") as arquivo:
        emails = arquivo.read()
    emails = emails.split('\n')
    emails = [email for email in emails if len(email) > 4]
    emails = list(set(emails))
    emails = [email.lower().strip() for email in emails]

    emails_cadastrar = []
    for email in emails:
        emails_cadastrar.append(
            models.EmailCliente(
                email=email,
                fase='Fase 3'
            )
        )
    models.EmailCliente.objects.bulk_create(emails_cadastrar)

    return redirect('index')

def cadastrar_emails(request):
    df_emails = pd.read_csv("Configuracoes/emails_cadastrados.csv")
    emails_cadastrados = [str(x) for x in df_emails["e-mails"].unique().tolist()]

    emails_cadastrar = []
    for email in emails_cadastrados:
        emails_cadastrar.append(
            core_models.Advogado(
                email=email,
            )
        )
    core_models.Advogado.objects.bulk_create(emails_cadastrar)

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