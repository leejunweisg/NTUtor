from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from listings.utility import fetch_modules, populate_modules
from listings import views as listing_views

# Create your views here.

# home page
@login_required()
def home(request):
    # Get filters
    studentType = ''
    if not request.GET.get('tutorFilter', None) == None:
        studentType = 'Tutor'
    if not request.GET.get('tuteeFilter', None) == None:
        studentType = 'Tutee'

    tutorFilterQuery = request.GET.get('tutorFilter')
    tuteeFilterQuery = request.GET.get('tuteeFilter')
    ratingsFilterQuery = request.GET.get('ratingsFilter')
    codeFilterQuery = request.GET.get('codeFilter')
    nameFilterQuery = request.GET.get('nameFilter')

    # If filter is none, return as ''
    if ratingsFilterQuery is None:
        ratingsFilterQuery = ''
    if codeFilterQuery is None:
        codeFilterQuery = ''
    if nameFilterQuery is None:
        nameFilterQuery = ''

    context = {
        'tuitionListings': listing_views.getTuitionListings(studentType, codeFilterQuery, nameFilterQuery, ratingsFilterQuery),
        'ratingsFilterQuery': ratingsFilterQuery,
        'codeFilterQuery': codeFilterQuery,
        'nameFilterQuery': nameFilterQuery
   }

    return render(request, 'listings/allListings.html', context)

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