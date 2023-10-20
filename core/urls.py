from django.urls import path

from . import views
urlpatterns = [ 
    path('', views.DashBoard.as_view(), name='index'),
    path('Fase1', views.Fase1.as_view(), name='fase1'),























    # path('visualizar/<str:estado>/', views.VisualizarDados.as_view(), name='visualizar_dados'),
    # path('cadastrar/<str:database>', views.Cadastrar.as_view(), name='cadastrar'),
    # path('filtros', views.Filtros.as_view(), name='filtros'),
    # path('historico/atual', views.ProdutoAtual.as_view(), name='hist_atual'),
    # path('produto/futuro', views.ProdutoFuturo.as_view(), name='produto_futuro'),
    # path("stopthread", views.StopThread.as_view(), name="stopthread"),
    # path("filtrar_produto_atual", views.FiltrarProdutoAtual.as_view(), name="filtrar_produto_atual"),
    # path('substituir_nomes', views.SubstituirNomes.as_view(), name='substituir_nomes'),

    # ############parciais render ######################
    # path('messages/messages', views.Messages.as_view(), name='messages'),
    # path('spinner/spinner', views.spinner, name='spinner'),

    # ########## CSV ################
    # path('csv/<int:type>', views.csv_download, name="csv"),
    # path('csv_filtrado', views.csv_produto_filtrado_download, name="csv_filtrado"),
    # path('cadastra_colunas', views.cadastra_nomes, name='cadastra_colunas')
]