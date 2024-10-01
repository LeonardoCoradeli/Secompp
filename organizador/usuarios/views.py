from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import get_user_model
from django import forms

# Obter o modelo de usuário personalizado
CustomUser = get_user_model()

# Formulário de criação de usuário
class UserCreationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password_app = forms.CharField(label='Password App', widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['email', 'password', 'password_app']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuário criado com sucesso!')
            return redirect('home')
        else:
            messages.error(request, 'Erro ao criar usuário. Verifique os dados e tente novamente.')
    else:
        form = UserCreationForm()

    return render(request, 'registration/register.html', {'form': form})

def home(request):
    return render(request, 'home/home.html')