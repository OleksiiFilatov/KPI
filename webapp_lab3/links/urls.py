"""linksite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from chat import consumer
from django.urls import re_path
from tinytask import consumer as counsumer_task

websocket_urlpatterns = [
    re_path(r'chat/ws/$', consumer.ChatConsumer.as_asgi()),
    re_path(r'task/ws/$', counsumer_task.TaskViewConsumer.as_asgi()),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('chat.urls')),
    path('', include('tinytask.urls')),
    path('', include('tinyurl.urls'))
]
