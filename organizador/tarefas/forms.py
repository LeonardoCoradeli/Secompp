from django import forms
from .models import Task, TaskLine

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title']

class TaskLineForm(forms.ModelForm):
    class Meta:
        model = TaskLine
        fields = ['text']