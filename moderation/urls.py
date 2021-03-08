from django.urls import path
from . import views

urlpatterns = [
    path('moderation/', views.moderation, name='moderation-home'),
    path('moderation/approve/<str:username>/', views.moderation_approve, name='approve'),
    path('moderation/reject/<str:username>/', views.moderation_reject, name='reject'),
]