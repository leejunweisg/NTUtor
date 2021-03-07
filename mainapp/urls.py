from django.db import models
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('', include('listings.urls')),
    path('moderation/', views.moderation, name='moderation-home'),
    path('moderation/approve/<str:username>/', views.moderation_approve, name='approve'),
    path('moderation/reject/<str:username>/', views.moderation_reject, name='reject'),
    path('403/', views.error403, name='error-403'),
    path('refreshmodules1236172/', views.refresh_modules, name='refresh-modules'), # do not go to this URL unnecessarily
]
