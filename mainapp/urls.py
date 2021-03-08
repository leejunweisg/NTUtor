from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('refreshmodules1236172', views.refresh_modules, name='refresh-modules'), # do not go to this URL unnecessarily
    path('users', include('users.url')),
]
