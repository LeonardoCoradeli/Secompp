from django.urls import path
from . import views

urlpatterns = [
    path('', views.listEmails, name='list_emails'),
    path('add-category/', views.add_category, name='add_category'),
    path('load-emails/', views.load_emails, name='load_emails'),
]
