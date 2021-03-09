from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import LoginView, LogoutView
from .forms import UserRegisterForm

from listings.utility import fetch_modules, populate_modules
from listings import views as listing_views

# moderation
from moderation import views as moderation_views

# Create your views here.


# log in page
class LoginFormView(SuccessMessageMixin, LoginView):
    template_name='accounts/login.html'
    success_message = f"Welcome, you are successfully logged in!"

    def get(self, request, *args, **kwargs):
        # if user is already signed in, redirect back to home
        if request.user.is_authenticated:
            messages.success(request, f"You are already signed in!")
            return redirect('home')
        return super().get(request, *args, **kwargs)

# log out view (doesn't render anything, just redirects to login)
class LogoutFormView(SuccessMessageMixin, LogoutView):
    success_message = f"You have been successfully logged out!"

# user registration page
def register(request):
    # if user is already signed in, redirect back to home
    if request.user.is_authenticated:
        messages.success(request, f"You are already signed in!")
        return redirect('home')

    if request.method == "POST":
        form = UserRegisterForm(request.POST)

        # email validation done on forms.py
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"Your account has been created! Please sign in!", )
            return redirect("login")
        else:                
            return render(request, 'accounts/register.html', {'form': form})
    else:
        form = UserRegisterForm()

    return render(request, 'accounts/register.html', {'form': form})

# error 403 page, displayed when an unauthorized user tries to access moderation pages
def error403(request):
    return render(request, 'page-403.html')

# refresh modules when view is called
@user_passes_test(lambda user: user.is_superuser)
def refresh_modules(request):
    if not fetch_modules:
        messages.error(request, f"Not successful in fetching modules!")
    else:
        if not populate_modules():
            messages.error(request, f"Not successful in populating modules!")
        else:
            messages.success(request, f"Successfully refreshed modules!")
    return render(request, 'index.html')