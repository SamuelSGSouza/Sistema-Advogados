from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, View
from django.contrib import messages
from django.contrib.messages import get_messages

from RPA.fase_1.pdf_extractor import main_extrator

#View inicial do sistema
class DashBoard(TemplateView):
    template_name = "core/dashboard.html"
    def get(self, *args, **kwargs):
        context = {
            'emails_cadastrados': 0,
            'emails_clientes': 0,
            'emails_negativos': 0,
            'dados_finais': 0,
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

        #salvando os arquivos na pasta RPA/fase_1
        files = []
        for arquivo in arquivos:
            file = 'RPA/fase_1/'+arquivo.name 
            with open(file, 'wb+') as destination:
                for chunk in arquivo.chunks():
                    destination.write(chunk)
            files.append(file)

        main_extrator(files)
        return redirect('fase1')


