from . import views
from django.urls import path



urlpatterns = [
    path('<str:key>/send/', views.webhook, name="webhook"),
    path('chat/', views.ChatView.as_view(), name='chat'),
    path('chat/users/', views.ChatUsersView.as_view(), name='chat-users'),
]

from .models import ConnectedUsers
ConnectedUsers.objects.all().delete()
