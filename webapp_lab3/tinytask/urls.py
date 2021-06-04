from . import views
from django.urls import path

urlpatterns = [
    path('adminTask/', views.AdminTaskView.as_view(), name='adminTask'),
    path('accounts/stats/', views.StatisticDataView.as_view(), name='user-stats')
]
# 