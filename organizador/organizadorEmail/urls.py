from django.urls import path
from . import views

urlpatterns = [
    path('teste/', views.organizador, name='organizador'),
    path('',views.index,name='index'),
]