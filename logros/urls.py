from django.urls import path
from . import views

urlpatterns = [
    path('', views.logro_list, name='logro_list'),
]
