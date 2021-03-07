from django.urls import path, include
from . import views
from listings import views as listing_views

urlpatterns = [
    path('', views.home, name='home'),
    path('', include('listings.urls')),
    path('refreshmodules1236172', views.refresh_modules, name='refresh-modules'), # do not go to this URL unnecessarily
]
