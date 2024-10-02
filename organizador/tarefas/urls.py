from django.urls import path
from . import views
from .views import AddTaskView

urlpatterns = [
    # Página principal onde o grid de tarefas é exibido
    path('', views.task_list, name='task_list'),
    path('add-task/', AddTaskView.as_view(), name='add_task'),
]
