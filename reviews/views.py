from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from listings.utility import fetch_modules, populate_modules

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (ListView, CreateView,UpdateView)
from .models import Review
from users.models import Profile


# Create your views here.

#dummy data for def profile_review(request):
reviews = [
    {
        'reviewID':'1',
        'tuitionSession':{'listing':{'title':'CZ2003'}},
        'reviewee':'James',
        'reviewer':'Tom',
        'description':'Tech very good, highly recomended',
        'rating':'5/5'
    },{
        'reviewID':'2',
        'tuitionSession':{'listing':{'title':'CZ2002'}},
        'reviewee':'James',
        'reviewer':'admin123',
        'description':'At vero eos et accusamus et iusto odio dignissimos ducimus qui blanditiis praesentium voluptatum deleniti atque corrupti quos dolores et quas molestias excepturi sint occaecati cupiditate non provident, similique sunt in culpa qui officia deserunt mollitia animi, id est laborum et dolorum fuga.',
        'rating':'4/5'
    }
]

#to show all review data from the database dynamically
class ReviewListView(LoginRequiredMixin,ListView):
    model = Review
    #<app>/<model>_<viewtype>.html
    template_name = 'reviews/listing-reviews.html'
    context_object_name = 'reviews'
    #ordering = ['-date_posted']

#creating a review to database, currently cannot auto populate the reviewer to current user automatically because of how
#the model is created, requires a instance of a proile instead of a id
#this uses crispy forms, added require in settings.py and additional information to use bootstrap4 for crispy
class ReviewCreateView(LoginRequiredMixin,CreateView):
    model = Review
    template_name = 'reviews/review_form.html'
    fields = [ 'tuitionSession','reviewee','description','rating']
    #success_url = 'reviews/'
    def form_valid(self,form):
            my_p = Profile.objects.get(user_id=self.request.user)
            form.instance.reviewer = my_p;
            return super().form_valid(form);
#https://stackoverflow.com/questions/35567667/cannot-assign-simplelazyobject-user-xxx-comment-user-must-be-a-mypro
#for getting instance of user profile     

        

class ReviewUpdateView(LoginRequiredMixin,UpdateView):
    model = Review
    template_name = 'reviews/review_form.html'
    fields = [ 'tuitionSession','reviewee','description','rating']
    #success_url = '../../'
   
    def form_valid(self,form):
        my_p = Profile.objects.get(user_id=self.request.user)
        form.instance.reviewer = my_p;
        return super().form_valid(form);


# review page using dummy data
@login_required()
def profile_review(request):

    # data to pass into page
    context = {
        'reviews':reviews
    }
    # render page
    # defines the template to render and the context to pass into the template
    return render(request, 'reviews/listing-reviews.html', context)


@login_required()
def add_review(request):

    # data to pass into page
    context = {}

    # render page
    # defines the template to render and the context to pass into the template
    return render(request, 'reviews/add-review.html', context)




