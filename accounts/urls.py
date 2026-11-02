from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('verify-2fa/', views.verify_2fa, name='verify_2fa'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('profile/', views.profile, name='profile'),
    path('enviar-recordatorios/', views.enviar_recordatorios_view, name='enviar_recordatorios'),
]
