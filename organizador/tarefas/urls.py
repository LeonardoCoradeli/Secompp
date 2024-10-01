from django.urls import path
from . import views

urlpatterns = [
    # Página principal onde o grid de tarefas é exibido
    path('', views.task_list, name='task_list'),
]
