from django.urls import path
from . import views

urlpatterns = [
    path('', views.portal_inicio, name='portal_inicio'),
    path('caballo/<int:pk>/', views.portal_caballo, name='portal_caballo_propietario'),
]
