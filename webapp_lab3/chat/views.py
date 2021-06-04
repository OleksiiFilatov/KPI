from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls.base import reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from channels.layers import get_channel_layer
from tinyurl.models import tinyURL
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.core.exceptions import PermissionDenied
from asgiref.sync import async_to_sync
from .models import ConnectedUsers

class ChatView(LoginRequiredMixin, TemplateView):
    template_name = 'chat/chat.html'
    title = 'chat'

class ChatUsersView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    template_name = 'chat/chat-users.html'
    title = 'chat-users'   
    paginate_by = 5

    def get_queryset(self):
        queryset = ConnectedUsers.objects.all().order_by('-connected')
        return queryset

    def test_func(self):
        return self.request.user.is_staff 
    

def webhook(request, key):
    object = get_object_or_404(tinyURL, src=key)
    if request.user != object.user:
        raise PermissionDenied 
    channel_layer = get_channel_layer()
    if not channel_layer.groups:
        return HttpResponse('No any groups available')
    async_to_sync(channel_layer.group_send)(
        list(channel_layer.groups.keys())[0], {
            'type' : "chat_link",
            "src": object.src,
            "dst": object.dst,
            "counter": object.counter,
            "name": request.user.username,
        })
    return HttpResponse("Send in chat")