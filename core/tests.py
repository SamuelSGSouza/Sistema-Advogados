from django.test import TestCase
import pandas as pd
from core import models as core_models, views as core_views
from RPA.fase_1 import pdf_extractor
from configs import models

class TestFase1(TestCase):
    quantidade_termos_categorias = 0
    df_data = None

    def setUp(self) -> None:
        core_views.cadastrar_termos()
        core_views.cadastrar_termos_negativos()
        self.quantidade_termos_categorias = models.TermoCategoria.objects.filter().count()
        models.TermoCaptura.objects.create(termo='nomeio',)

    def test_fase_1_verifica_quantidade_termos_categorias_nao_eh_zero(self,):
        ''' Aqui irei testar se a quantidade de termos que classificam
            a categoria de um processo é maior que zero'''
        self.assertGreater(self.quantidade_termos_categorias, 0)

    def test_fase_1_verifica_quantidade_termos_captura_nao_eh_zero(self,):
        ''' Aqui irei testar se a quantidade de termos que classificam
            a categoria de um processo é maior que zero'''
        quantidade_termos_captura = models.TermoCaptura.objects.filter().count()
        self.assertGreater(quantidade_termos_captura, 0)

    def test_fase_1_gera_processos(self,):
        ''' Aqui irei testar se a execução da fase 1 gera os processos corretamente'
            e os cadastra no banco de dados.'''
        pdf_files = ['test_files/1.pdf', ]
        quantidade_antes = core_models.Processo.objects.count()
        self.df_data = pdf_extractor.main_extrator(pdf_files)
        quantidade_depois = core_models.Processo.objects.count()
        self.assertGreater(quantidade_depois, quantidade_antes)

    def test_fase_1_gera_processos_repetidos(self,):
        ''' Aqui irei testar se a execução da fase 1 gera os processos corretamente'
            e os cadastra no banco de dados.'''
        #verificando se o model de processos com "_teste_" possui numeros repetidos
        processos = self.df_data["numero_judicial"].values
        
        #verificando se existem processos repetidos
        self.assertEqual(len(processos), len(set(processos)))

    def test_fase_1_pega_categoria_e_classe(self,):
        ''' Aqui irei testar se os processos encontrados na fase 1 possuem categoria e classe
            corretamente.'''
        #verificando se o model de processos com "_teste_" possui numeros repetidos
        df = self.df_data
        #verificando se todos possuem categoria e classe
        categoria_e_classe = df["classe"].notnull().all() and df["categoria"].notnull().all()
        self.assertTrue(categoria_e_classe)

    def test_fase_1_pega_processos_nao_identificados(self,):
        ''' Aqui irei testar se os processos não identificados são realmente processos
            que não foram encontrados na fase 1.'''
        #verificando se o model de processos com "_teste_" possui numeros repetidos
        df = self.df_data
        #verificando se todos possuem categoria e classe
        processos_nao_identificados = df[df["categoria"] == "Processos não Identificados"]
        self.assertEqual(len(processos_nao_identificados), 0)