"""
URL configuration for dietlense project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
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
from diet_app.views import *
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup',Signup.as_view()),
    path('token',obtain_auth_token),
    path('create-profile',Profileview.as_view()),
    path('profile/<int:pk>',Profileretrive.as_view()),
    path('user/<int:pk>',UserRetriveview.as_view()),
    path('foodlog',Foodlogcreatedlistview.as_view()),
    path('foodlogs/<int:pk>',FoodlogRetriveUpdateDestroy.as_view()),
    path('summery',Dietsummery.as_view())

]
