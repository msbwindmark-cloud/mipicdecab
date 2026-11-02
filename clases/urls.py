from django.urls import path
from . import views

urlpatterns = [
    path('', views.clase_list, name='clase_list'),
    path('crear/', views.clase_create, name='clase_create'),
]
