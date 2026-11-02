from django.urls import path
from . import views

urlpatterns = [
    path('', views.chat_panel, name='chat_panel'),
    path('<int:pk>/', views.chat_conversacion, name='chat_conversacion'),
    path('<int:pk>/enviar/', views.chat_enviar, name='chat_enviar'),
]
