from django.urls import path
from . import views

urlpatterns = [
    path('', views.propietario_list, name='propietario_list'),
    path('exportar/excel/', views.exportar_propietarios_excel, name='exportar_propietarios_excel'),
    path('<int:pk>/', views.propietario_detail, name='propietario_detail'),
    path('crear/', views.propietario_create, name='propietario_create'),
    path('<int:pk>/editar/', views.propietario_update, name='propietario_update'),
]
