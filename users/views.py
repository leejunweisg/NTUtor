from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Avg
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import UpdateView

# import models that are accessed in this view
from django.contrib.auth.models import User
from .models import Profile
from listings.models import Listing
from reviews.models import Review
from .forms import ProfileUpdateForm

# Create your views here.
@login_required
def profile(request, username):

    # if the request originates from the owner
    owner = (request.user.username == username)

    # find user
    profile = User.objects.get(username=username).profile

    # get profile details
    profile_details = {}
    profile_details['id'] = profile.id
    profile_details['name'] = profile.name
    profile_details['username'] = profile.user.username
    profile_details['email'] = profile.user.email
    profile_details['num_listings'] = Listing.objects.filter(user=profile).count()
    profile_details['verified'] = profile.verified == 1
    profile_details['desc'] = profile.description
    profile_details['image'] = profile.image
    avg_rating = Review.objects.filter(reviewee=profile).aggregate(Avg('rating'))['rating__avg']
    profile_details['avg_rating'] = avg_rating if avg_rating is not None else 'N/A'

    # get listings for profile
    tuition_listings = []
    request_listings = []

    all_listings = profile.listing_set.all().order_by('-listingID')

    for row in all_listings:
        temp = {}

        temp['title'] = row.title
        temp['module'] = row.module
        temp['datePosted'] = row.datePosted
        temp['id'] = row.listingID

        if row.typeOfListing == 'Providing':
            tuition_listings.append(temp)
        else:
            request_listings.append(temp)

    context = {'profile_details': profile_details,
                'tuitionListings': tuition_listings,
                'requestListings': request_listings}
                
    return render(request, 'users/profile.html', context)

# TODO: EDIT PROFILE
@login_required
def editprofile(request):
    return render(request, 'users/editprofile.html')

@login_required
def want_verified(request):
    profile = request.user.profile

    # check if user was already approved
    if profile.verified == 1:
        messages.warning(request, 'You are already a <strong>Verified Tutor</strong> <i class="fa fa-check-circle" aria-hidden="true" data-toggle="tooltip" data-placement="top" title="Verified Tutor"></i> !')
    elif profile.verified == -1:
        messages.warning(request, "You have already submitted a request, a moderator will review your request soon!")
    # modify verified value in database
    else:
        profile.verified = -1
        profile.save()
        result = True
        messages.success(request, "Successful, your request has been sent!")

    # render
    return redirect('home')

@login_required
def UpdateProfile(request):
    # form submission
    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid:
            form.save()
            messages.success(request, f"Your profile has been updated!")
            return redirect('profile', request.user.username)
    # else, render form
    else:
        form = ProfileUpdateForm(instance=request.user.profile)
        context = {'form': form}

    return render(request, 'users/profile_update.html', context)