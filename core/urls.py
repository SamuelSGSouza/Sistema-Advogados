from django.urls import path

from . import views
urlpatterns = [ 
    path('', views.DashBoard.as_view(), name='index'),
    path('Fase1', views.Fase1.as_view(), name='fase1'),
    path('Fase2', views.Fase2.as_view(), name='fase2'),
    path('Fase3', views.Fase3.as_view(), name='fase3'),


    path('cadastrar_termos', views.cadastrar_termos, name='cadastrar_termos'),
    path("cadastrar_termos_negativos", views.cadastrar_termos_negativos, name="cadastrar_termos_negativos"),
    path("cadastrar_sec_desejadas", views.cadastrar_sec_desejadas, name="cadastrar_sec_desejadas"),
]