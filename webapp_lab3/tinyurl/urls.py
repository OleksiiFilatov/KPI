from django.urls import path
from django.urls.conf import include
from . import views
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token

router = routers.DefaultRouter()
router.register(r'groups', views.GroupViewSet)
router.register(r'urls', views.tinyURLViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/api-token-auth/', obtain_auth_token),
    path('', views.MainView.as_view(), name='main'),
    path('accounts/profile/', views.ProfileView.as_view(), name='profile'),
    path('accounts/register/', views.RegisterView.as_view(), name='register'),
    path('accounts/login/', views.LoginView.as_view(), name='login'),
    path('accounts/logout/', views.LogoutView.as_view(), name='logout'),
    path('accounts/links/', views.tinyURLListView.as_view(), name='links'),
    path('accounts/links/make', views.tinyURLCreateView.as_view(), name='makeLink'),
    path('<str:key>/', views.RedirectView.as_view(), name='redirect'),
    path('<str:key>/delete/', views.DeleteRedirectView.as_view(), name='redirectDelete')
]