from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from listings.utility import fetch_modules, populate_modules

# Create your views here.

# home page
@login_required()
def home(request):

    # data to pass into page
    context = {}

    # render page
    # defines the template to render and the context to pass into the template
    return render(request, 'index.html', context)

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
