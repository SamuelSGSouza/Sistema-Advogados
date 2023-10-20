from django.urls import path

from . import views
urlpatterns = [ 
    path('', views.DashBoard.as_view(), name='index'),
    path('Fase1', views.Fase1.as_view(), name='fase1'),


    path('cadastrar_termos', views.cadastrar_termos, name='cadastrar_termos'),
    path("cadastrar_termos_negativos", views.cadastrar_termos_negativos, name="cadastrar_termos_negativos"),
]