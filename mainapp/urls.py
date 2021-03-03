from django.urls import path

from . import views
from reviews import views as review_views
from reviews.views import ReviewListView, ReviewCreateView, ReviewUpdateView


urlpatterns = [
    path('', views.home, name='home'),
    path('refreshmodules1236172', views.refresh_modules, name='refresh-modules'), # do not go to this URL unnecessarily

    #using dummy data for this reviews
    path('reviews/', review_views.profile_review, name='reviews'), # built-in class-based views
    #currently nothign because using reviews/new/ but this is a function call
    path('add-review/',review_views.add_review ,name='add-review'),

    #class call using database data of reviews
    path('reviewsclass/', ReviewListView.as_view(), name='reviewsclass'),

    #class call for using database data
    path('reviews/new/', ReviewCreateView.as_view(), name='review-create'),
    path('reviews/<int:pk>/update/', ReviewUpdateView.as_view(), name='review-update')
    

]
