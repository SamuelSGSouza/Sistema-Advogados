from django.urls import path

from . import views
urlpatterns = [ 
    path('', views.DashBoard.as_view(), name='index'),
    path('Fase1', views.Fase1.as_view(), name='fase1'),
    path('Fase2', views.Fase2.as_view(), name='fase2'),
    path('Fase3', views.Fase3.as_view(), name='fase3'),
    path('todas_fases', views.TodasFases.as_view(), name='todas_fases'),
    path('gera_e_retorna_csv', views.gera_e_retorna_csv, name='gera_e_retorna_csv'),


    path('cadastrar_termos', views.cadastrar_termos, name='cadastrar_termos'),
    path('cadastrar_emails', views.cadastrar_emails, name='cadastrar_emails'),
    path('cadastrar_termos_negativos_nome_advogado', views.cadastrar_termos_negativos_nome_advogado, name='cadastrar_termos_negativos_nome_advogado'),
    path('cadastrar_termos_email_advogados', views.cadastrar_termos_email_advogados, name='cadastrar_termos_email_advogados'),
    path('cadastrar_emails_negativos', views.cadastrar_emails_negativos, name='cadastrar_emails_negativos'),
    path('termos_remocao_pagina_email', views.termos_remocao_pagina_email, name='termos_remocao_pagina_email'),
    path('cadastrar_nomes_masculinos', views.cadastrar_nomes_masculinos, name='cadastrar_nomes_masculinos'),
    path("cadastrar_termos_negativos", views.cadastrar_termos_negativos, name="cadastrar_termos_negativos"),
    path("cadastrar_sec_desejadas", views.cadastrar_sec_desejadas, name="cadastrar_sec_desejadas"),
]