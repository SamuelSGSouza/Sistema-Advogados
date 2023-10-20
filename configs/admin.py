from django.contrib import admin
from . import models

@admin.register(models.StatusFase)
class StatusFaseAdmin(admin.ModelAdmin):
    list_display = ('fase', 'status', "data_modificado")
    search_fields = ('fase', 'status', )
    list_filter = ('fase', )

@admin.register(models.TermoCategoria)
class TermoCategoriaAdmin(admin.ModelAdmin):
    list_display = ('termo', 'categoria', "fase")
    search_fields = ('termo', 'categoria', )
    list_filter = ('categoria', )

@admin.register(models.TermoCaptura)
class TermoCapturaAdmin(admin.ModelAdmin):
    list_display = ('termo', "fase")
    search_fields = ('termo', )

@admin.register(models.TermoNegativo)
class TermoNegativoAdmin(admin.ModelAdmin):
    list_display = ('termo', "fase")
    search_fields = ('termo', )

@admin.register(models.SecoesDesejadas)
class SecoesDesejadasAdmin(admin.ModelAdmin):
    list_display = ('secao', "fase")
    search_fields = ('secao', )

