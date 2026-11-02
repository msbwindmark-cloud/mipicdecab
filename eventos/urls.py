from django.urls import path
from . import views

urlpatterns = [
    path('', views.evento_list, name='evento_list'),
    path('crear/', views.evento_create, name='evento_create'),
    path('<int:pk>/', views.evento_detail, name='evento_detail'),
    path('<int:pk>/editar/', views.evento_update, name='evento_update'),
    path('<int:pk>/eliminar/', views.evento_delete, name='evento_delete'),
]
