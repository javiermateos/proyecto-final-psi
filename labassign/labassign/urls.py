"""labassign URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path

from core import views

urlpatterns = [
    path('', views.home, name='home'),
    path('index/', views.home, name='index'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('login_help/', views.login_help, name='login_help'),
    path('convalidation/', views.convalidation, name='convalidation'),
    path('convalidation_help/',
         views.convalidation_help,
         name='convalidation_help'),
    path('applypair/', views.apply_pair, name='applypair'),
    path('applypair_help/', views.applypair_help, name='applypair_help'),
    path('applygroup/', views.apply_group, name='applygroup'),
    path('applygroup_help/', views.applygroup_help, name='applygroup_help'),
    path('breakpair/', views.breakpair, name='breakpair'),
    path('help/', views.help, name='help'),
    path('admin/', admin.site.urls),
]
