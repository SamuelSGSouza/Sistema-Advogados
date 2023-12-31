from django.db import models

class StatusFase(models.Model):
    """ Aqui serão inseridos os status de cada fase."""
    fase = models.CharField(max_length=255, verbose_name='Fase')
    status = models.CharField(max_length=255, verbose_name='Status')
    data_modificado = models.DateTimeField(auto_now=True, verbose_name='Data de Modificação')

############## MODELS FASE 1 #####################
class TermoCaptura(models.Model):
    """ Aqui serão inseridos os termos que, caso sejam encontrados num
        dos parágrafos durante a leitura do processo, ele será coletado."""
    termo = models.CharField(max_length=255, verbose_name='Termo de Nomeação')
    fase = models.CharField(max_length=255, verbose_name='Fase', default='Fase 1')

class TermoNegativo(models.Model):
    """ Aqui serão inseridos os termos que, caso sejam encontrados num
        dos parágrafos durante a leitura do processo, ele não será coletado."""
    termo = models.CharField(max_length=255, verbose_name='Termo Negativo')
    fase = models.CharField(max_length=255, verbose_name='Fase', default='Fase 1')

class TermoCategoria(models.Model):
    """ Aqui serão inseridos os termos que, caso sejam encontrados num
        dos parágrafos durante a leitura do processo, ele será considerado
        daquela categoria."""
    termo = models.CharField(max_length=255, verbose_name='Termo de Categoria', unique=True)
    categoria = models.CharField(max_length=255, verbose_name='Categoria')
    fase = models.CharField(max_length=255, verbose_name='Fase', default='Fase 1')

############## MODELS FASE 2 #####################
class SecoesDesejadas(models.Model):
    """ Aqui serão inseridos as seções que serão coletadas do site
        do processo."""
    secao = models.CharField(max_length=255, verbose_name='Seção')
    fase = models.CharField(max_length=255, verbose_name='Fase', default='Fase 2')
    

############## MODELS FASE 3 #####################
class NomesMasculinos(models.Model):
    """ Aqui serão inseridos os nomes masculinos que serão usados
        para identificar os gêneros."""
    nome = models.CharField(max_length=255, verbose_name='Nome Masculino')
    fase = models.CharField(max_length=255, verbose_name='Fase', default='Fase 3')

class TermosRemocaoPaginaEmail(models.Model):
    """ Aqui serão inseridos os termos que, caso sejam encontrados
        na página de e-mail, ela será removida."""
    termo = models.CharField(max_length=255, verbose_name='Termo de Remoção')
    fase = models.CharField(max_length=255, verbose_name='Fase', default='Fase 3')

class EmailsNegativos(models.Model):
    """ Aqui serão inseridos os e-mails que não serão coletados."""
    email = models.CharField(max_length=255, verbose_name='E-mail de Remoção')
    fase = models.CharField(max_length=255, verbose_name='Fase', default='Fase 3')

class TermosEmailAdvogados(models.Model):
    """ Aqui serão inseridos os termos que, caso sejam encontrados
        no email a ser distribuído, ele será considerado email de advogado."""
    termo = models.CharField(max_length=255, verbose_name='Termo de Remoção')
    fase = models.CharField(max_length=255, verbose_name='Fase', default='Fase 3')

class TermoNegativoNomeAdvogado(models.Model):
    """ Aqui serão inseridos os termos que, caso sejam encontrados
        no nome do advogado, o termo será removido"""
    termo = models.CharField(max_length=255, verbose_name='Termo de Remoção')
    fase = models.CharField(max_length=255, verbose_name='Fase', default='Fase 3')

class EmailCliente(models.Model):
    """ Aqui serão inseridos os emails dos clientes."""
    email = models.CharField(max_length=255, verbose_name='E-mail do Cliente')
    fase = models.CharField(max_length=255, verbose_name='Fase', default='Fase 3')
    
