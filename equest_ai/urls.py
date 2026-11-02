from django.urls import path
from . import views

urlpatterns = [
    path('', views.equest_ai_home, name='equest_ai_home'),
    path('responder/', views.equest_ai_responder, name='equest_ai_responder'),
]
