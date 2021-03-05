from django.shortcuts import render
from django.db.models import Avg

from users.models import Profile
from listings.models import TuitionSession
from reviews.models import Review

def get_verified_requests():
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

    return results

def approve(username):
    try:
        # find the user
        profile = Profile.objects.get(user__username=username)

        # check if user was already approved
        if profile.verified == 1:
            return "The user was already approved!"
        # modify verified value
        else:
            profile.verified = 1
            profile.save()
            return True

    # if user not found (only can happen if someone modified request URL)
    except Profile.DoesNotExist:
        return "The user was not found!"

def reject(username):
    try:
        # find the user
        profile = Profile.objects.get(user__username=username)

        # check if user was already rejected
        if profile.verified == 0:
            return "The user was already rejected!"
        # modify verified value
        else:
            profile.verified = 0
            profile.save()
            return True

    # if user not found (only can happen if someone modified request URL)
    except Profile.DoesNotExist:
        return "The user was not found!"
