from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    # URL de login
    path('login/', auth_views.LoginView.as_view(),name='login'),

    # URL de logout
    path('logout/', auth_views.LogoutView.as_view(),name='logout'),

    # URL de mudança de senha (opcional)
    path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),

    # URL de reset de senha (opcional)
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/{uuid32}/{token}/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    
    #URL de cadastro
    path('register/', views.register, name='register'),
    
    #URL da home
    path('home/', views.home, name='home'),
]
