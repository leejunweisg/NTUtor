from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required()
def home(request):

    # data to pass into page
    context = {}

    # render page
    # defines the template to render and the context to pass into the template
    return render(request, 'index.html', context)