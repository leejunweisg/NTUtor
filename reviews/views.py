from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from listings.utility import fetch_modules, populate_modules

from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.views.generic import (ListView, CreateView,UpdateView,DeleteView)
from .models import Review
from users.models import Profile



# Create your views here.

#to show all review data from the database dynamically
class ReviewListView(LoginRequiredMixin,ListView):
    model = Review
    #<app>/<model>_<viewtype>.html
    template_name = 'reviews/listing-reviews.html'
    context_object_name = 'reviews'

    def get_context_data(self, **kwargs):
        #Call base implementation first to get a context
        context = super(ReviewListView, self).get_context_data(**kwargs)
        #Add extra context, student profile
        context['studentProfile'] = Profile.objects.get(user_id=self.request.user)
        return context
    #ordering = ['-date_posted']


class ReviewListViewByUsername(LoginRequiredMixin,ListView):
    
    model = Review
    template_name = 'reviews/listing-reviews-username.html'
    context_object_name = 'reviews'
    

    def get_context_data(self,**kwargs):
        context = super(ReviewListViewByUsername, self).get_context_data(**kwargs)
        context['studentProfile'] = Profile.objects.get(user_id=self.request.user)
        currentProfile = Profile.objects.get(user_id=self.request.user)
        currentID = currentProfile.id
        context['tutorid'] = self.kwargs['tutorid']

        selectedUserid = self.kwargs['tutorid']
        tutor = Profile.objects.get(id=selectedUserid)
        
        context['tutorName'] = tutor.name
        return context

    

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

        

class ReviewUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = Review
    template_name = 'reviews/review_form.html'
    fields = [ 'tuitionSession','reviewee','description','rating']
    #success_url = '../../'
   
    def form_valid(self,form):
        my_p = Profile.objects.get(user_id=self.request.user)
        form.instance.reviewer = my_p;
        return super().form_valid(form);
    
    def test_func(self):
        my_p = Profile.objects.get(user_id=self.request.user)
        if self.get_object().reviewer == my_p:
            return True
        return False

class ReviewDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = Review
    template_name = 'reviews/review_confirm_delete.html'
    success_url = "/"
    def test_func(self):
        my_p = Profile.objects.get(user_id=self.request.user)
        if self.get_object().reviewer == my_p:
            return True
        return False
    






