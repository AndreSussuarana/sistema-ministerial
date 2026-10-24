from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path

urlpatterns = [ # type:ignore
    path('admin/', admin.site.urls),
    path('login/', auth_views.LoginView.as_view(template_name='pautas/login.html'), name='login'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='pautas/password_reset.html'), name='password_reset'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='pautas/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='pautas/password_reset_complete.html'), name='password_reset_complete'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('pautas/', include('pautas.urls')),
]