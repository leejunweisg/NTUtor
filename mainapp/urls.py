from django.urls import path
from .views import register, LoginFormView, LogoutFormView, error403, refresh_modules
from .forms import CustomLoginForm

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', LoginFormView.as_view(authentication_form=CustomLoginForm), name='login'),
    path('logout/', LogoutFormView.as_view(), name='logout'),
    path('403/', error403, name='error-403'),
    path('refreshmodules1236172/', refresh_modules, name='refresh-modules'), # DO NOT go to this URL unnecessarily
]
