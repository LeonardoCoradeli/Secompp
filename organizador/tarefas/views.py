from django.http import JsonResponse
from django.shortcuts import render, redirect,get_object_or_404
from tarefas.models import Task, TaskLine,UserTask
from django.contrib.auth import get_user_model
from usuarios.models import CustomUser
import json
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
import uuid
from django.contrib import messages
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
    return render(request, 'tasks/tasks.html', {'task':context})

@method_decorator(csrf_exempt, name='dispatch')
class AddTaskView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            task_title = data.get('taskTitle')
            task_lines = data.get('taskLines', [])

            if not task_title:
                return JsonResponse({'status': 'error', 'message': 'Task title is required'}, status=400)

            # Obter o usuário logado
            usuario = request.user

            # Criar a nova tarefa
            task = Task.objects.create(
                taskId=uuid.uuid4(),
                title=task_title,
                systemSmartDelete=False
            )

            # Associar a tarefa ao usuário
            UserTask.objects.create(
                userId=usuario,
                taskId=task
            )

            # Criar as linhas de tarefa
            for line in task_lines:
                TaskLine.objects.create(
                    taskLineId=uuid.uuid4(),
                    taskId=task,
                    text=line['taskLineText'],
                    is_done=line['taskLineCheckbox']
                )

            return JsonResponse({'status': 'success', 'message': 'Tarefa criada com sucesso'}, status=201)
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    
