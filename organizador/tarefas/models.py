from django.db import models
from usuarios.models import BaseControlModel
from django.contrib.auth import get_user_model
from uuid import uuid4
from django.utils import timezone
CustomUser = get_user_model()

class Task(BaseControlModel):
    taskId = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    title = models.CharField(max_length=50)
    due_date = models.DateTimeField()

    def __str__(self):
        return self.title
    
class TaskLine(BaseControlModel):
    taskLineId = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    taskId = models.ForeignKey(Task, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    is_done = models.BooleanField(default=False)
    due_date = models.DateTimeField()
    def __str__(self):
        return self.title
    
class UserTask(models.Model):
    userId = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user_tasks')
    taskId = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='user_tasks')

    def __str__(self):
        return f'{self.userId} - {self.taskId}'

