from django.urls import path

from . import views
from reviews import views as review_views
from reviews.views import ReviewListView, ReviewCreateView, ReviewUpdateView, ReviewDeleteView


urlpatterns = [
    #class call using database data of reviews
    path('reviews/', ReviewListView.as_view(), name='reviews'),
    #class call for using database data
    path('reviews/new/', ReviewCreateView.as_view(), name='review-create'),
    path('reviews/<int:pk>/update/', ReviewUpdateView.as_view(), name='review-update'),
    path('reviews/<int:pk>/delete/', ReviewDeleteView.as_view(), name='review-delete')
    

]
