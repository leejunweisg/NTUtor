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
    # returns true if modified
    # return false if not modified

    # find the user
    profile = Profile.objects.get(user__username=username)
    if profile:
        print("user found:" + profile.user.username)
        profile['verified'] = 1
        profile.save()
        print("saved!")
        return True
    #TODO: profile mmatching query does not exist
    else:
        print("user not found...")
        return False