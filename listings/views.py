from django.shortcuts import render
from django.db.models import Avg
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from operator import itemgetter
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger 

# import models that are accessed in this view
from .models import Listing, Module, TuitionSession
from users.models import Profile
from reviews.models import Review

# home page 2
@login_required()
def listings(request):

    # Get filters
    tuitionFilterQuery = request.GET.get('tuitionFilter')
    requestFilterQuery = request.GET.get('requestFilter')
    ratingsFilterQuery = request.GET.get('ratingsFilter')
    codeFilterQuery = request.GET.get('codeFilter')
    nameFilterQuery = request.GET.get('nameFilter')

    # set listing type
    listingType = ''
    if tuitionFilterQuery == 'on' and requestFilterQuery == 'on':
        listingType = ''
    elif tuitionFilterQuery == 'on':
        listingType = 'Tuition'
    elif requestFilterQuery == 'on':
        listingType = 'Request'

    # If filter is none, return as ''
    if ratingsFilterQuery is None or ratingsFilterQuery == 'Any':
        ratingsFilterQuery = ''
    if codeFilterQuery is None:
        codeFilterQuery = ''
    if nameFilterQuery is None:
        nameFilterQuery = ''

    tuitionListings = getTuitionListings(listingType, codeFilterQuery, nameFilterQuery, ratingsFilterQuery)
    
    page = request.GET.get('page', 1)

    # Set how many listings per page
    paginator = Paginator(tuitionListings, 10)
    
    try:
        tuitionListings = paginator.page(page)
    except PageNotAnInteger:
        tuitionListings = paginator.page(1)
    except EmptyPage:
        tuitionListings = paginator.page(paginator.num_pages)

    top3List = getTopRatedTutors()
    
    context = {
        'top3Tutors' : top3List,
        'tuitionListings': tuitionListings,
        'ratingsFilterQuery': request.GET.get('ratingsFilter'),
        'codeFilterQuery': codeFilterQuery,
        'nameFilterQuery': nameFilterQuery
   }

    return render(request, 'listings/listings.html', context)

# home page
@login_required()
def home(request):

    # latest tuition listings
    tuition_listings = getLatestListings('Providing')

    # latest request listings
    request_listings = getLatestListings('Requesting')

    # top three rated tutors
    top_3_tutors = getTopRatedTutors()
    
    # set context
    context = {
        'top3Tutors' : top_3_tutors,
        'tuitionListings': tuition_listings,
        'requestListings': request_listings
   }

    # rener
    return render(request, 'listings/home.html', context)

# returns 10 latest listings
def getLatestListings(listing_type):
    latest_listings = Listing.objects.filter(typeOfListing=listing_type).order_by('-listingID')[:10]

    latest_listings_list = []

    for row in latest_listings:
        temp = {}

        temp['title'] = row.title
        temp['module'] = row.module
        temp['name'] = row.user.name # name from profile model
        temp['username'] = row.user.user.username
        temp['poster_id'] = row.user.user.id # added by sam #TODO: what is this for
        
        temp['datePosted'] = row.datePosted
        temp['id'] = row.listingID

        # avg rating
        avg_rating = Review.objects.filter(reviewee=row.user).aggregate(Avg('rating'))['rating__avg']
        temp['avg_rating'] = avg_rating if avg_rating is not None else 'N/A'

        latest_listings_list.append(temp)

    return latest_listings_list

# Check if search box is empty
def isValidQuery(param):
    return param != '' and param is not None

# Get listing by the student type user is looking for, e.g. finding a tutor or finding a tutee
# Get listing by module code or module name
# Get listing by ratings user want and above
def getTuitionListings(studentType, moduleCode, moduleName, ratings):
    #Get all tuition listings
    allListings = Listing.objects.all()
    
    # Filter by the 3 filters before converting to list
    if isValidQuery(studentType):
        allListings = allListings.filter(typeOfListing=studentType)

    if isValidQuery(moduleCode):
        allListings = allListings.filter(module__moduleCode__icontains = moduleCode)

    if isValidQuery(moduleName):
        allListings = allListings.filter(module__moduleName__icontains = moduleName)
    
    #Convert to list 
    allListingsList = []
    
    for r in allListings:
        temp = {}

        temp['title'] = r.title
        temp['typeOfStudent'] = r.typeOfListing
        temp['datePosted'] = r.datePosted
        temp['username'] = r.user.user.username
        temp['poster_id'] = r.user.user.id # added by sam
        temp['name'] = r.user.name
        temp['id'] = r.listingID

        userRatings = []
        #Find avg ratings for user
        for p in Profile.objects.all():
            temp2 = {}
            temp2['username'] = p.user.username
            temp2['sessions'] = TuitionSession.objects.filter(tutor = p, completed = True).count()
            temp2['reviews'] = Review.objects.filter(reviewee=p).count()
            avg_rating = Review.objects.filter(reviewee=p).aggregate(Avg('rating'))['rating__avg']
            temp2['avgRating'] = avg_rating if avg_rating is not None else -1
            userRatings.append(temp2)

        #Check if username matches, then append rating
        for u in userRatings:
            if u['username'] == temp['username']:
                temp['avgRating'] = u['avgRating']

        #Then find module code & name of listing
        temp['module'] = r.module

        #Append to list
        allListingsList.append(temp)

    # Filter by ratings
    if isValidQuery(ratings):
        allListingsList = [i for i in allListingsList if int(i['avgRating']) >= int(ratings)]

    return allListingsList

# get top rated tutors
def getTopRatedTutors():
    results = []

    # retrieve profiles
    for p in Profile.objects.all():
        temp = {}

        # get info
        temp['username'] = p.user.username
        temp['name'] = p.name
        temp['verified'] = p.verified

        # number of tuition sessions given
        temp['n_sessions'] = TuitionSession.objects.filter(tutor=p, completed=True).count()

        # number of reviews received
        temp['n_reviews'] = Review.objects.filter(reviewee=p).count()

        # avg rating
        avg_rating = Review.objects.filter(reviewee=p).aggregate(Avg('rating'))['rating__avg']
        temp['avg_rating'] = avg_rating if avg_rating is not None else -1
        temp['image'] = p.image
        
        results.append(temp)

    results = sorted(results, key = itemgetter('avg_rating'), reverse=True)
    results = results[:3]
    return results

def getOneTuitionListing(listingID):
    listingInfo = Listing.objects.get(listingID = listingID)
    return listingInfo

def getStudentDetails(username):
    studentDetailsList = {}
    studentDetails = Profile.objects.filter(user__username = username)

    for p in studentDetails:
        studentDetailsList['id'] = p.user.id #added by sam
        studentDetailsList['username'] = p.user.username
        studentDetailsList['email'] = p.user.email
        studentDetailsList['name'] = p.name
        studentDetailsList['description'] = p.description
        studentDetailsList['image'] = p.image
        studentDetailsList['verified'] = p.verified

        # Get avg ratings for student as a tutor
        sessionsTutor = TuitionSession.objects.filter(tutor = p, completed = True).count()
        reviewsTutor = Review.objects.filter(reviewee = p).count()
        avgRatingTutor = Review.objects.filter(reviewee = p).aggregate(Avg('rating'))['rating__avg']
        avgRatingTutor = avgRatingTutor if avgRatingTutor is not None else 'N/A'
        studentDetailsList['avgRatingTutor'] = avgRatingTutor
    
        # Get avg ratings for student as a tutee
        sessionTutee = TuitionSession.objects.filter(learner = p, completed = True).count()
        reviewsTutee = Review.objects.filter(reviewee = p).count()
        avgRatingTutee = Review.objects.filter(reviewee = p).aggregate(Avg('rating'))['rating__avg']
        avgRatingTutee = avgRatingTutee if avgRatingTutee is not None else 'N/A'
        studentDetailsList['avgRatingTutee'] = avgRatingTutee

        # Get total listings
        studentDetailsList['totalListings'] = Listing.objects.filter(user = p).count()
    
    return studentDetailsList

# Class to view one listing
class ListingDetailView(DetailView):
    model = Listing
    fields = ['title', 'module', 'typeOfStudent', 'datePosted', 'description']

    def get_context_data(self, **kwargs):
        username = self.get_object().user.user.username
        #Call base implementation first to get a context
        context = super(ListingDetailView, self).get_context_data(**kwargs)
        #Add extra context, student profile
        context['studentProfile'] = getStudentDetails(username)
        return context

# Class to make form for create tuition listing
class ListingCreateView(LoginRequiredMixin, CreateView):
    model = Listing
    fields = ['title', 'description', 'module', 'typeOfListing']

    # Get username and submit form
    def form_valid(self, form):
        form.instance.user = Profile.objects.get(user_id = self.request.user)
        return super().form_valid(form)

# Class to make form for update tuition listing
class ListingUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Listing
    fields = ['title', 'description']
    template_name_suffix = '_update_form'
    slug_url_kwarg = 'listingID'

    # Get username and submit form
    def form_valid(self, form):
        form.instance.user = Profile.objects.get(user_id = self.request.user)
        return super().form_valid(form)

    # Only creator of listing can update listing
    def test_func(self):
        if self.get_object().user.user == self.request.user:
            return True
        return False

class ListingDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Listing
    success_url = '/'

    # Only creator of listing can delete listing
    def test_func(self):
        if self.get_object().user.user == self.request.user:
            return True
        return False