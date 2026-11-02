from django.urls import path
from . import views

urlpatterns = [
    path('', views.encuesta_list, name='encuesta_list'),
    path('crear/', views.encuesta_create, name='encuesta_create'),
    path('<int:pk>/', views.encuesta_detail, name='encuesta_detail'),
    path('<int:pk>/editar/', views.encuesta_update, name='encuesta_update'),
    path('<int:pk>/eliminar/', views.encuesta_delete, name='encuesta_delete'),
]
