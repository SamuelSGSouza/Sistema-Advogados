from django.db import models

class Processo(models.Model):
    numero_judicial = models.CharField(max_length=20, primary_key=True, verbose_name='Número Judicial')
    vara = models.CharField(max_length=255, verbose_name='Vara', null=True, blank=True)
    valor_causa = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Valor da Causa', null=True, blank=True)
    classe = models.CharField(max_length=255, verbose_name='Classe')
    categoria = models.CharField(max_length=255, verbose_name='Categoria')
    assunto = models.CharField(max_length=255, verbose_name='Assunto', null=True, blank=True)
    area = models.CharField(max_length=255, verbose_name='Área', null=True, blank=True)
    requerente = models.CharField(max_length=255, verbose_name='Requerente', null=True, blank=True)
    requerido = models.CharField(max_length=255, verbose_name='Requerido', null=True, blank=True)
    juiz = models.CharField(max_length=255, verbose_name='Juiz', null=True, blank=True)
    situacao_processo = models.CharField(max_length=255, verbose_name='Situação do Processo', null=True, blank=True)
    perito = models.CharField(max_length=255, verbose_name='Perito', null=True, blank=True)
    status = models.CharField(max_length=255, verbose_name='Status', null=True, blank=True)
    data_cadastro = models.DateTimeField(auto_now_add=True, verbose_name='Data de Cadastro no Sistema')

class Advogado(models.Model):
    email = models.EmailField(max_length=255, primary_key=True, verbose_name='E-mail')
    nome = models.CharField(max_length=255, verbose_name='Nome')
    nome_cliente = models.CharField(max_length=255, verbose_name='Nome do Cliente')
    oab = models.CharField(max_length=255, verbose_name='OAB', null=True, blank=True)
    email_secundario = models.EmailField(max_length=255, verbose_name='E-mail Secundário', null=True, blank=True)
    possiveis_emails = models.CharField(max_length=255, verbose_name='Possíveis E-mails', null=True, blank=True)
    email_distribuido = models.BooleanField(verbose_name='E-mail Distribuído', default=False)
    telefones = models.CharField(max_length=255, verbose_name='Telefones', null=True, blank=True)
    sites = models.CharField(max_length=255, verbose_name='Sites', null=True, blank=True)
    data_cadastro = models.DateTimeField(auto_now_add=True, verbose_name='Data de Cadastro no Sistema')