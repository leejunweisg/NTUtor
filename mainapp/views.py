from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from listings.utility import fetch_modules, populate_modules
from listings import views as listing_views

# moderation
from moderation import views as moderation_views

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