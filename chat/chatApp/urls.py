from django.urls import path
from .views import *

urlpatterns = [
    path('', logIn, name='login'),
    path('dashboard', dashboard, name="dashboard"),
    path('admin_login', adminLogIn, name='admin_login'),
    path('admin_dashboard', adminDashboard, name="admin_dashboard"),
]
