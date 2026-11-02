from django.urls import path
from . import views

urlpatterns = [
    path('', views.desparasitacion_list, name='desparasitacion_list'),
    path('registrar/', views.registrar_desparasitacion, name='registrar_desparasitacion'),
    path('plan/', views.plan_create, name='plan_create'),
    path('plan/<int:pk>/', views.plan_detail, name='plan_detail'),
    path('plan/<int:pk>/editar/', views.plan_update, name='plan_update'),
    path('plan/<int:pk>/eliminar/', views.plan_delete, name='plan_delete'),
    path('registro/<int:pk>/', views.registro_detail, name='registro_detail'),
    path('registro/<int:pk>/editar/', views.registro_update, name='registro_update'),
    path('registro/<int:pk>/eliminar/', views.registro_delete, name='registro_delete'),
]
