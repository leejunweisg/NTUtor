from django.urls import path
from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt
from . import views

urlpatterns = [
	path ('viewprofile', views.profile, name = 'profilepage'),
	path ('editprofile', views.editprofile, name = 'editprofilepage'),
	url(r'^users/editprofile', csrf_exempt('users.views.updateprofile')),
]