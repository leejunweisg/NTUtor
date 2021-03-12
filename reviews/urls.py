from django.urls import path

from . import views
from reviews import views as review_views
from reviews.views import ReviewListView, ReviewCreateView, ReviewUpdateView, ReviewDeleteView,ReviewListViewByUsername


urlpatterns = [
    #class call using database data of reviews
    path('allreviews/', ReviewListView.as_view(), name='reviews'),
    path('reviews/<int:tutorid>/', ReviewListViewByUsername.as_view(), name='reviews-username'),
    #class call for using database data
    path('reviews/new/', ReviewCreateView.as_view(), name='review-create2'),
    path('reviews/<int:pk>/update/', ReviewUpdateView.as_view(), name='review-update'),
    path('reviews/<int:pk>/delete/', ReviewDeleteView.as_view(), name='review-delete'),

    path('reviews/new/<int:user>/<int:listingID>', ReviewCreateView.as_view(), name='review-create'),
    

]
