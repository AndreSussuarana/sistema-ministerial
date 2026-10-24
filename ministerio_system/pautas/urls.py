from django.contrib.auth import views as auth_views
from django.urls import path, reverse_lazy

from . import views

app_name = 'pautas'

urlpatterns = [ # type:ignore
    path('', views.listar_pautas, name='listar_pautas'),
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

    # Rotas de Recuperação de Palavra-passe
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='pautas/password_reset.html', success_url=reverse_lazy('pautas:password_reset_done')), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='pautas/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='pautas/password_reset_confirm.html', success_url=reverse_lazy('pautas:password_reset_done')), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='pautas/password_reset_complete.html'), name='password_reset_complete'),
]