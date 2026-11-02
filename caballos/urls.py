from django.urls import path
from . import views

urlpatterns = [
    path('', views.caballo_list, name='caballo_list'),
    path('exportar/excel/', views.exportar_caballos_excel, name='exportar_caballos_excel'),
    path('<int:pk>/', views.caballo_detail, name='caballo_detail'),
    path('crear/', views.caballo_create, name='caballo_create'),
    path('<int:pk>/editar/', views.caballo_update, name='caballo_update'),
    path('<int:pk>/eliminar/', views.caballo_delete, name='caballo_delete'),
    path('<int:pk>/qr/', views.caballo_qr, name='caballo_qr'),
    path('<int:pk>/galeria/', views.galeria_caballo, name='galeria_caballo'),
    path('<int:pk>/ficha-clinica-pdf/', views.ficha_clinica_pdf, name='ficha_clinica_pdf'),
    path('<int:pk>/historial-economico/', views.historial_economico, name='historial_economico'),
    path('<int:pk>/control-peso/', views.control_peso, name='control_peso'),
]
