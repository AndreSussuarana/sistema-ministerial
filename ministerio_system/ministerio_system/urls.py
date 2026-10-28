from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path, reverse_lazy
from django.views.generic import RedirectView
from pautas import views

urlpatterns = [ # type:ignore
    path('', RedirectView.as_view(pattern_name='login', permanent=False)),
    path('admin/', admin.site.urls),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='pautas/login.html'), name='login'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='pautas/password_reset.html'), name='password_reset'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='pautas/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='pautas/password_reset_complete.html'), name='password_reset_complete'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('pautas/', include('pautas.urls')),
    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='pautas/password_reset.html', 
        success_url=reverse_lazy('password_reset_done')
    ), name='password_reset'),
    
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='pautas/password_reset_done.html'
    ), name='password_reset_done'),
    
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='pautas/password_reset_confirm.html', 
        success_url=reverse_lazy('password_reset_complete')
    ), name='password_reset_confirm'),
    
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='pautas/password_reset_complete.html'
    ), name='password_reset_complete'),
]