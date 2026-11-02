from django.urls import path
from . import views

urlpatterns = [
    path('<int:caballo_id>/', views.timeline_caballo, name='timeline_caballo'),
]
