from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('', logIn, name='logIn'),
    path('adminlogin', adminLogIn, name='adminlogin'),  # noqa
    path('dashboard', dashboard, name="userdashboard"),  # noqa
    path('admindashboard', adminDashboard, name="admindashboard"),  # noqa
]
