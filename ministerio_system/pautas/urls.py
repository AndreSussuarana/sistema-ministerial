
from django.urls import path

from . import views

app_name = 'pautas'

urlpatterns = [ # type:ignore
    path('', views.dashboard, name='dashboard'),
    path('pautas', views.listar_pautas, name='listar_pautas'),
    path('nova/', views.criar_pauta, name='criar_pauta'),
    path('<int:pk>/', views.detalhe_pauta, name='detalhe_pauta'), # type:ignore
    path('<int:pk>/editar/', views.editar_pauta, name='editar_pauta'),

    path('reunioes/', views.listar_reunioes, name='listar_reunioes'),
    path('reunioes/nova/', views.criar_reuniao, name='criar_reuniao'),
    path('reunioes/<int:pk>/', views.detalhe_reuniao, name='detalhe_reuniao'),
    path('reunioes/<int:pk>/editar/', views.editar_reuniao, name='editar_reuniao'),
    
    path('reunioes/<int:pk>/modo-reuniao/', views.modo_reuniao, name='modo_reuniao'),
    path('reunioes/<int:pk>/ata/', views.gerar_ata, name='gerar_ata'),
    path('reunioes/<int:pk>/concluir/', views.concluir_reuniao, name='concluir_reuniao'),
]