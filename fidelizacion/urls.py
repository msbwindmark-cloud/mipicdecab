from django.urls import path
from . import views

urlpatterns = [
    path('', views.fidelizacion_list, name='fidelizacion_list'),
    path('recompensa/', views.recompensa_list, name='recompensa_list'),
    path('recompensa/crear/', views.recompensa_create, name='recompensa_create'),
    path('recompensa/<int:pk>/', views.recompensa_detail, name='recompensa_detail'),
    path('recompensa/<int:pk>/editar/', views.recompensa_update, name='recompensa_update'),
    path('recompensa/<int:pk>/eliminar/', views.recompensa_delete, name='recompensa_delete'),
    path('movimiento/', views.movimiento_list, name='movimiento_list'),
    path('movimiento/crear/', views.movimiento_create, name='movimiento_create'),
    path('movimiento/<int:pk>/', views.movimiento_detail, name='movimiento_detail'),
    path('movimiento/<int:pk>/editar/', views.movimiento_update, name='movimiento_update'),
    path('movimiento/<int:pk>/eliminar/', views.movimiento_delete, name='movimiento_delete'),
]
