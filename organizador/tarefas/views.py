from django.http import JsonResponse
from django.shortcuts import render, redirect,get_object_or_404
from tarefas.models import Task, TaskLine,UserTask
from django.contrib.auth import get_user_model
from usuarios.models import CustomUser
import json

CustomUser = get_user_model()

def getContextUtil(request):
    email = request.user.email
    # Busca o objeto do usuário no banco de dados
    usuario = get_object_or_404(CustomUser, email=email)
    # Filtra os ids das tarefas associadas ao usuário
    tasks_ids = UserTask.objects.filter(userId=usuario.userId).values_list('taskId', flat=True)
    # Busca as tarefas e linhas de tarefas relacionadas aos ids
    tasks = Task.objects.filter(taskId__in=tasks_ids,systemSmartDelete=False)
    tasks_lines = TaskLine.objects.filter(taskId__in=tasks_ids)
    
    context = []
    for task in tasks:
        task_lines = [
            {
                'taskLineId': line.taskLineId,
                'taskLineText': line.text,
                'taskLineCheckbox': line.is_done
            }
            for line in tasks_lines if line.taskId == task
        ]
        context.append({
            'taskId': task.taskId,
            'taskTitle': task.title,
            'taskLines': task_lines
        })
        
    print(context)
    return context

def task_list(request):
    context = getContextUtil(request)
    return render(request, 'tasks/tasks.html', {'tasks':context})

def update_task(request, task_id, task_line_id,context):
    # Buscar a linha de tarefa pelo ID
    task_line = get_object_or_404(TaskLine, taskLineId=task_line_id, taskId=task_id)
    
    if request.method == 'POST':
        # Atualizar o estado do checkbox de acordo com o que foi enviado na página
        task_line.is_done = not task_line.is_done
        task_line.save()
        
    context = getContextUtil(request)
    return render(request, 'tasks/tasks.html', context)
    
