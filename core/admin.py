from django.contrib import admin
from . import models

@admin.register(models.Processo)
class ProcessoAdmin(admin.ModelAdmin):
    list_display = ('numero_judicial', 'classe', 'categoria', )
    search_fields = ('numero_judicial', 'classe', 'categoria', )
    list_filter = ('categoria', 'status' )

@admin.register(models.Advogado)
class AdvogadoAdmin(admin.ModelAdmin):
    list_display = ("email", 'nome', )
    search_fields = ("email", 'nome',  )