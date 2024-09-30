from django.shortcuts import render
from django.http import HttpResponse
from organizadorEmail.models import CustomUser

def criarUsuario(request):
    CustomUser.objects.create_user()