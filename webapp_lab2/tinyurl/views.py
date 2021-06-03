from django.views.generic.edit import FormView, DeleteView, CreateView
from django.views.generic.base import TemplateView, RedirectView
from django.views.generic import ListView
from .forms import SignUpForm
from django.shortcuts import get_object_or_404
from django.contrib.auth import login, authenticate, views as authViews
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import tinyURL
from django.http import HttpResponseRedirect
from django.core.exceptions import PermissionDenied
from django.db.models import F
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from .serializers import GroupSerializer, tinyURLSerializer
from rest_framework import mixins

class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all().order_by('-id')
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAdminUser]


class tinyURLViewSet(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   viewsets.GenericViewSet):
    """
    API endpoint that allows links to be viewed or edited.
    """
    queryset = tinyURL.objects.all().order_by('-creation_time')
    serializer_class = tinyURLSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user = self.request.user)

class tinyURLCreateView(LoginRequiredMixin,CreateView):
    template_name = 'tinyurl/makeLink.html'
    model = tinyURL
    fields = ['dst']

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        context = self.get_context_data(form=form)
        return self.render_to_response(context)
            

class tinyURLListView(LoginRequiredMixin, ListView):
    template_name = 'tinyurl/tinylist.html'
    paginate_by = 5

    def get_queryset(self):
        return tinyURL.objects.filter(user = self.request.user).order_by('-creation_time')

class DeleteRedirectView(LoginRequiredMixin, DeleteView):
    model = tinyURL
    success_url = reverse_lazy('links')

    def delete(self, request, *args, **kwargs):
        self.object = get_object_or_404(tinyURL, src=kwargs['key'])
        if request.user != self.object.user:
            raise PermissionDenied 
        self.object.delete()
        return HttpResponseRedirect(self.success_url)

class RedirectView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        link = get_object_or_404(tinyURL, src=kwargs['key'])
        link.counter = F("counter") + 1
        link.save(update_fields=["counter"])
        return link.dst

class MainView(TemplateView):
    template_name = 'tinyurl/home.html'

class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'tinyurl/profile.html'

class RegisterView(FormView):
    template_name = 'tinyurl/register.html'
    form_class = SignUpForm
    success_url = reverse_lazy('profile')
    
    def form_valid(self, form):
        user = form.save()
        user.refresh_from_db()
        user.profile.date_of_birth = form.cleaned_data.get('date_of_birth')
        user.profile.gender = form.cleaned_data.get('gender')
        user.save()
        login(self.request, user)
        return super().form_valid(form)

class LoginView(authViews.LoginView):
    template_name = 'tinyurl/login.html'

class LogoutView(authViews.LogoutView):
    next_page = '/'
    