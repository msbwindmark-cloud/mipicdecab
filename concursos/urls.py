from django.urls import path
from . import views

urlpatterns = [
    path('', views.concurso_list, name='concurso_list'),
    path('crear/', views.concurso_create, name='concurso_create'),
    path('<int:pk>/', views.concurso_detail, name='concurso_detail'),
    path('<int:pk>/editar/', views.concurso_update, name='concurso_update'),
    path('<int:pk>/eliminar/', views.concurso_delete, name='concurso_delete'),
]
