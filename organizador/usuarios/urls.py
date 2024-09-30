from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    # URL de login
    path('login/', auth_views.LoginView.as_view()),

    # URL de logout
    path('logout/', auth_views.LogoutView.as_view()),

    # URL de mudança de senha (opcional)
    path('password_change/', auth_views.PasswordChangeView.as_view()),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view()),

    # URL de reset de senha (opcional)
    path('password_reset/', auth_views.PasswordResetView.as_view()),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view()),
    path('reset/{uuid32}/{token}/', auth_views.PasswordResetConfirmView.as_view()),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view()),
    
    #URL de cadastro
    path('register/', views.register, name='register'),
]
