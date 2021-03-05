from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from listings.utility import fetch_modules, populate_modules

# moderation
from moderation import views as moderation_views

# Create your views here.

# home page
@login_required()
def home(request):

    # data to pass into page
    context = {}

    # render page
    # defines the template to render and the context to pass into the template
    return render(request, 'index.html', context)

# moderation home page
@user_passes_test(lambda user: user.groups.filter(name = "Moderators").exists(), login_url='error-403')
def moderation(request):
    context = {}
    context['verified_requests'] = moderation_views.get_verified_requests()
    return render(request, 'moderation/moderation.html', context)

# approve a verified request
@user_passes_test(lambda user: user.groups.filter(name = "Moderators").exists(), login_url='error-403')
def moderation_approve(request, username=None):
    context = {}
    result = moderation_views.approve(username)
    if result == True:
        messages.success(request, "Successful, the user has been approved!")
    else:
        messages.warning(request, result)
    return redirect('moderation-home')

# reject a verified request
@user_passes_test(lambda user: user.groups.filter(name = "Moderators").exists(), login_url='error-403')
def moderation_reject(request, username=None):
    context = {}
    result = moderation_views.reject(username)
    if result == True:
        messages.success(request, "Successful, the user has been rejected!")
    else:
        messages.warning(request, result)
    return redirect('moderation-home')

# error 403 page, displayed when unauthorized user tries to access moderation pages
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