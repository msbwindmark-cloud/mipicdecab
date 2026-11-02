from django.urls import path
from . import views

urlpatterns = [
    path('', views.factura_list, name='factura_list'),
    path('morosos/', views.morosos, name='morosos'),
    path('exportar/excel/', views.exportar_facturas_excel, name='exportar_facturas_excel'),
    path('crear/', views.factura_create, name='factura_create'),
    path('<int:pk>/', views.factura_detail, name='factura_detail'),
    path('cobrar/<int:pk>/', views.factura_cobrar, name='factura_cobrar'),
    path('<int:pk>/pdf/', views.factura_pdf, name='factura_pdf'),
]
