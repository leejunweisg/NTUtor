from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home(request):

    # data to pass into page
    context = {}

    # render page
    # defines the template to render and the context to pass into the template
    return render(request, 'mainapp/home.html', context)

