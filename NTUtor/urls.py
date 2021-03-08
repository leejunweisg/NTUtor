"""NTUtor URL Configuration

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
from users import views as user_views
from users.forms import CustomLoginForm

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', user_views.register, name='register'),
    path('login/', user_views.LoginFormView.as_view(authentication_form=CustomLoginForm), name='login'), # built-in class-based views
    path('logout/', user_views.LogoutFormView.as_view(), name='logout'), # built-in class-based views
    path('', include('mainapp.urls')), # include urls.py from mainapp!
    path('users/', include('users.url')),
]
