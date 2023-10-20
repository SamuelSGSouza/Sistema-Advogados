import threading
import time
from datetime import timedelta

import pandas as pd
import os
from django.conf import settings
from . import models
from . import functions

import traceback

class ExecutaFaseThread(threading.Thread):
    def __init__(self, functions:list, request, error):
        self.funcoes = functions
        self.request = request
        self.erro = error
        self.situacao = ''
        self.tempo_total=0
        threading.Thread.__init__(self)

    
    def run(self):
        # try:
            start = time.time()
            objs = self.funcoes[0]()
            lista_gerada = time.time() - start
            self.situacao = f"Lista de dados gerada em {lista_gerada:.2f} Segundos."
            ini = time.time()
            self.funcoes[1](objs)
            self.error = {'ok': True}
            self.tempo_total = str(timedelta(seconds = int(time.time() - ini)))

        # except Exception as e:
        #     if self.erro['ok'] == True:
        #         self.erro = {'ok':False, 'msg': f'Erro do tipo {type(e)}. Erro: {e}'}

class AtualizaThread(threading.Thread):
    '''Esta classe é responsável por gerenciar as funções para criação de produto
    ATUAL e produto PASSADO'''
    def __init__(self, function, request, error={'ok':True}, reiniciar=False):
        self.funcao = function
        self.request = request
        self.erro = error
        self.situacao = ''
        self.estado = ''
        self.reiniciar = reiniciar
        self.valor_inicio = 0
        self.tempo_total = 0
        self.parar = False
        threading.Thread.__init__(self)

    
    def run(self):
        # try:
            print("Estou na AtualizaThread")
            ini = time.time()
            self.situacao = f"Processo de geração de usuários iniciado."
            if self.reiniciar:
                print("Reiniciando...")
                #excluindo tudo da tabela atual
                atual = models.ProdutoFinalAtual.objects.filter()
                atual._raw_delete(atual.db)
                self.situacao = f"Eliminei tudo da tabela anterior."
                self.estado = "AC"
                self.valor_inicio = 0
                self.reiniciar = False
            else:
                status = models.Status.objects.filter().first()
                self.estado = status.estado
                self.valor_inicio = status.valor_inicio
                self.situacao = f"Processo de geração de usuários continuando no estado {self.estado} e valor anterior {status.valor_inicio}."

            df = pd.DataFrame()
            
            functions.baixa_telefones(self)

            #começando a lista a partir do self.estado
            estados = estados[estados.index(self.estado):]
            # estados = ["AM",'ES', "MG", "RJ", "SP", "FN" ]
            
            for estado in estados:
                print(estado)
                if self.parar:
                    return "Processo parado pelo usuário."

                ################# Gerando Salvamento de status #################
                self.estado = estado
                self.valor_inicio = 0
                status = models.Status.objects.filter().first()
                status.estado = self.estado
                status.valor_inicio = self.valor_inicio
                status.save()
                ################################################################
                self.situacao = self.situacao + f' - Cadastrando dados para {estado}'
                qtd, sit, df_atual = self.funcao(estado, self)
                if qtd != 0:
                    self.situacao = sit
                else:
                    self.situacao = str(self.situacao).split(' - ')[0]
                print()
                
                if type(df_atual) != str:
                    if df.empty:
                        df = df_atual
                    df = pd.concat([df, df_atual], axis=0)
            print("VERIFIQUEI TODOS OS ESTADOS")
            ################# Gerando Salvamento de status #################
            self.estado = "AC"
            self.valor_inicio = 0
            status = models.Status.objects.filter().first()
            status.estado = self.estado
            status.valor_inicio = self.valor_inicio
            status.save()
            ################################################################

            functions.cria_csvs()
            print("CRIEI OS CSVs")
            self.tempo_total = str(timedelta(seconds = int(time.time() - ini))) 

        # except Exception as e:
        #     if self.erro['ok'] == True:
        #         self.erro = {'ok':False, 'msg': f'Erro do tipo {type(e)}. Erro: {e}'}

class AtualizaThreadFutura(threading.Thread):
    def __init__(self, function, request, error={'ok':True}):
        self.funcao = function
        self.request = request
        self.erro = error
        self.situacao = ''
        self.tempo_total=0
        threading.Thread.__init__(self)

    
    def run(self):
       pass

class GeraCSV(threading.Thread):
    def __init__(self, function, writer, qs):
        self.writer = writer
        self.function = function
        self.qs = qs
        threading.Thread.__init__(self)


    
    def run(self):
        retorno = self.function(self.writer, self.qs)
        return retorno
    

class FiltrarProdutoAtualThread(threading.Thread):
    def __init__(self, functions:list, request, error):
        self.funcoes = functions
        self.request = request
        self.erro = error
        self.situacao = ''
        self.tempo_total=0
        threading.Thread.__init__(self)

    
    def run(self):
        try:
            print("Estou na FiltrarProdutoAtualThread")
            start = time.time()
            filtragem = self.funcoes[0]()
            if not filtragem['ok']:
                self.erro = {'ok': False, 'msg': filtragem['msg']}
                return None

            lista_gerada = time.time() - start
            self.situacao = f"Lista de dados gerada em {lista_gerada:.2f} Segundos."
            ini = time.time()
            self.funcoes[1]()
            self.error = {'ok': True}
            self.tempo_total = str(timedelta(seconds = int(time.time() - ini)))

        except Exception as e:
            if self.erro['ok'] == True:
                self.erro = {'ok':False, 'msg': f'Erro do tipo {type(e)}. Erro: {traceback.format_exc()}'}