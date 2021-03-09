from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Avg

# import models that are accessed in this view
from users.models import Profile
from listings.models import TuitionSession
from reviews.models import Review

# moderation home page
@user_passes_test(lambda user: user.groups.filter(name = "Moderators").exists(), login_url='error-403')
def moderation(request):
    results = []

    # retrieve profiles with verified==-1 and loop
    for p in Profile.objects.filter(verified="-1"):
        temp = {}

        # get username
        temp['username'] = p.user.username

        # number of tuition sessions given
        temp['n_sessions'] = TuitionSession.objects.filter(tutor=p, completed=True).count()

        # number of reviews received
        temp['n_reviews'] = Review.objects.filter(reviewee=p).count()

        # avg rating
        avg_rating = Review.objects.filter(reviewee=p).aggregate(Avg('rating'))['rating__avg']
        temp['avg_rating'] = avg_rating if avg_rating is not None else 'N/A'

        results.append(temp)
    
    # render
    return render(request, 'moderation/moderation.html', {'verified_requests': results})

# approve a verified request
@user_passes_test(lambda user: user.groups.filter(name = "Moderators").exists(), login_url='error-403')
def moderation_approve(request, username=None):
    try:
        # find the user
        profile = Profile.objects.get(user__username=username)

        # check if user was already approved
        if profile.verified == 1:
            messages.warning(request, "The user was already approved!")

        # modify verified value in database
        else:
            profile.verified = 1
            profile.save()
            result = True
            messages.success(request, "Successful, the user has been approved!")

    # if user not found (only can happen if someone modified request URL)
    except Profile.DoesNotExist:
        messages.warning(request, "The user was not found!")

    # render
    return redirect('moderation-home')

# reject a verified request
@user_passes_test(lambda user: user.groups.filter(name = "Moderators").exists(), login_url='error-403')
def moderation_reject(request, username=None):
    try:
        # find the user
        profile = Profile.objects.get(user__username=username)

        # check if user was already rejected
        if profile.verified == 0:
            messages.warning(request, "The user was already rejected!")
        # modify verified value
        else:
            profile.verified = 0
            profile.save()
            messages.success(request, "Successful, the user has been rejected!")

    # if user not found (only can happen if someone modified request URL)
    except Profile.DoesNotExist:
        return "The user was not found!"

    # render
    return redirect('moderation-home')
