from typing import Any
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib import messages

from configs import models
from . import models as core_models
from core import tasks
import os
import pandas as pd
import datetime

from django.http import FileResponse
from django.contrib.auth.mixins import LoginRequiredMixin

import os
from django.conf import settings

def salvar_arquivos(arquivos):
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
    return files

class DashBoard(LoginRequiredMixin,TemplateView):
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

class Fase1(LoginRequiredMixin,TemplateView):
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
        if status.status == "Erro na execução":
            messages.error(self.request, f'Erro na execução em {status.data_modificado.strftime("%d/%m/%Y")} às {status.data_modificado.strftime("%H:%M:%S")}')
            
        context['status'] = status
        return context

    def post(self,*args, **kwargs):
        #pegando os arquivos pdfs enviados
        arquivos = self.request.FILES.getlist('arquivos')
        files = salvar_arquivos(arquivos)
    
        # main_extrator(files)
        models.StatusFase.objects.update_or_create(fase="Fase 1", status="Iniciado")
        tasks.processa_fase_1.delay(files)

        messages.success(self.request, 'Processo iniciado com sucesso! Recarregue a página para atualizar o status.')
        return redirect('fase1')

class Fase2(LoginRequiredMixin,TemplateView):
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
        if status.status == "Erro na execução":
            messages.error(self.request, f'Erro na execução em {status.data_modificado.strftime("%d/%m/%Y")} às {status.data_modificado.strftime("%H:%M:%S")}')
            
        context['status'] = status
        return context

    def post(self,*args, **kwargs):
        models.StatusFase.objects.update_or_create(fase="Fase 2", status="Iniciado")
        tasks.processa_fase_2.delay()

        messages.success(self.request, 'Processo iniciado com sucesso! Recarregue a página para atualizar o status.')
        return redirect('fase2')

class Fase3(LoginRequiredMixin,TemplateView):
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
        if status.status == "Erro na execução":
            messages.error(self.request, f'Erro na execução em {status.data_modificado.strftime("%d/%m/%Y")} às {status.data_modificado.strftime("%H:%M:%S")}')
            
        context['status'] = status
        return context

    def post(self,*args, **kwargs):
        model = models.StatusFase.objects.filter(fase="Fase 3").first()
        model.status = "Iniciado"
        model.save()
        
        tasks.processa_fase_3.delay()

        messages.success(self.request, 'Processo iniciado com sucesso! Recarregue a página para atualizar o status.')
        return redirect('fase3')

class TodasFases(LoginRequiredMixin,TemplateView):
    template_name = "core/todas_fases.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        status1  = models.StatusFase.objects.filter(fase="Fase 1").first().status
        status2 = models.StatusFase.objects.filter(fase="Fase 2").first().status
        status3 = models.StatusFase.objects.filter(fase="Fase 3").first().status

        #se um dos status for "processando", então o status geral é "processando"
        if status1 == "Processando" or status2 == "Processando" or status3 == "Processando":
            status = "Processando"
        else:
            status = "OK"
        context['status'] = status

        return context
    
    def post(self, *args, **kwargs):
        models.StatusFase.objects.all().delete()
        core_models.Advogado.objects.all().delete()
        core_models.Processo.objects.all().delete()
        models.StatusFase.objects.create(fase="Fase 1", status="Iniciado")
        models.StatusFase.objects.create(fase="Fase 2", status="Iniciado")
        models.StatusFase.objects.create(fase="Fase 3", status="Iniciado")

        arquivos = self.request.FILES.getlist('arquivos')
        files = salvar_arquivos(arquivos)
        tasks.processa_todas_fases.delay(files)

        messages.success(self.request, 'Processos iniciados com sucesso! Recarregue a página para atualizar o status.')
        return redirect('todas_fases')

def gera_e_retorna_csv(request):
    desejado = request.GET.get('desejado')
    if desejado == "hoje":
        #pegando todos os advogados cadastrados hoje
        advogados = core_models.Advogado.objects.filter(data_cadastro__date=datetime.date.today())
    else:
        advogados = core_models.Advogado.objects.all()
    
    #criando o dataframe
    df = pd.DataFrame(advogados.values())
    #criando as colunas
    df["vara"] = ""
    df["valor_causa"] = ""
    df["classe"] = ""
    df["categoria"] = ""
    df["assunto"] = ""
    df["area"] = ""
    df["requerente"] = ""
    df["requerido"] = ""
    df["juiz"] = ""
    df["situacao_processo"] = ""
    df["perito"] = ""

    #numeros_processos
    numeros_processos = df["processo"].unique().tolist()

    for numero in numeros_processos:
        print("numero: ", numero)
        processo = core_models.Processo.objects.get(numero_judicial=numero)
        df.loc[df["processo"] == numero, "vara"] = processo.vara
        df.loc[df["processo"] == numero, "valor_causa"] = processo.valor_causa
        df.loc[df["processo"] == numero, "classe"] = processo.classe
        df.loc[df["processo"] == numero, "categoria"] = processo.categoria
        df.loc[df["processo"] == numero, "assunto"] = processo.assunto
        df.loc[df["processo"] == numero, "area"] = processo.area
        df.loc[df["processo"] == numero, "requerente"] = processo.requerente
        df.loc[df["processo"] == numero, "requerido"] = processo.requerido
        df.loc[df["processo"] == numero, "juiz"] = processo.juiz
        df.loc[df["processo"] == numero, "situacao_processo"] = processo.situacao_processo
        df.loc[df["processo"] == numero, "perito"] = processo.perito

    #renomeando
    df.rename(columns={
        "numero_processo": "Processo Digital Nº",
        "classe": "Classe",
        "categoria": "Categoria",
        "assunto": "Assunto",
        "area": "Área",
        "requerente": "Requerente",
        "requerido": "Requerido",
        "advogado": "Nome do Advogado",
        "tratamento": "Tratamento",
        "email_advogado": "E-mail do Advogado",
        "email_2_advogado": "E-mail 2 do Advogado",
        "possiveis_emails_advogado": "Possíveis E-mails do Advogado",
        "telefones_advogado": "Telefones do Advogado",
        "sites_advogado": "Sites do Advogado",
        "cliente": "Nome do Cliente",
        "juiz(a)": "Juiz(a)",
        "vara": "Vara",
        "valor_processo": "Valor da Causa",
        "situacao_processo": "Situação do Processo",
        "perito": "Perito"
        }, inplace=True)
    
    #reordenando
    df = df[['Situacao Email_1/Email_2', 'Processo Digital Nº','Vara', 'Valor da Causa', 'Classe', 
             'Categoria', 'Assunto', 'Área', 'Requerente', 'Requerido', 'Tratamento', 
             'Nome do Advogado', "Email_Distribuido?", 'E-mail do Advogado', 'E-mail 2 do Advogado', 
             'Possíveis E-mails do Advogado','Nome do Cliente', 'Juiz(a)', 'Situação do Processo', 
             'Perito', 'Telefones do Advogado', 'Sites do Advogado']]

    #criando o nome do arquivo
    nome_arquivo = f"dados_{datetime.date.today()}.csv"
    #salvando o arquivo
    df.to_csv(f"media/{nome_arquivo}", index=False)
    #retornando o download
    response = FileResponse(f"media/{nome_arquivo}", content_type='text/csv')

    # Defina o cabeçalho Content-Disposition para indicar que é um download
    response['Content-Disposition'] = 'attachment; filename="{}"'.format(nome_arquivo)
    
    return response

def cadastrar_sec_desejadas(request):
    models.SecoesDesejadas.objects.all().delete()
    secoes = []
    with open("test_files/tipos_secoes.txt", "r", encoding="utf-8") as f:
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

def cadastrar_termos():
    #excluir todos os termos
    # models.TermoCategoria.objects.all().delete()
    with open("test_files/termos_contabilidade.txt", "r") as arquivo:
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
    

    with open("test_files/termos_engenharia.txt", "r") as arquivo:
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

    with open("test_files/termos_grafotecnica.txt", "r") as arquivo:
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
    with open("test_files/nomes_masculinos.txt", "r") as arquivo:
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
    with open("test_filestermos_remocao_pagina_email.txt", "r") as arquivo:
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
    with open("test_files/emails_negativos.txt", "r") as arquivo:
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
    with open("test_files/termos_email_advogado.txt", "r") as arquivo:
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
    with open("test_files/termos_negativos_nome_advogado.txt", "r") as arquivo:
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
    with open("test_files/emails_clientes.txt", "r") as arquivo:
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
    df_emails = pd.read_csv("test_files/emails_cadastrados.csv")
    emails_cadastrados = [str(x) for x in df_emails["e-mails"].unique().tolist()]

    emails_cadastrar = []
    for email in emails_cadastrados:
        emails_cadastrar.append(
            core_models.Advogado(
                email=email,
            )
        )
    core_models.Advogado.objects.bulk_create(emails_cadastrar)

def cadastrar_termos_negativos():
    with open("test_files/negative_keywords.txt", "r") as arquivo:
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