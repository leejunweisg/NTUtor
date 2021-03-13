from django.urls import path

from . import views
from reviews import views as review_views
from reviews.views import ReviewListView, ReviewCreateView, ReviewUpdateView, ReviewDeleteView,ReviewListViewByUsername,ReviewCreateViewWithId


urlpatterns = [
    #class call using database data of reviews
    path('allreviews/', ReviewListView.as_view(), name='reviews'),
    path('reviews/<int:tutorid>/', ReviewListViewByUsername.as_view(), name='reviews-username'),
    #class call for using database data

    path('reviews/new/', ReviewCreateView.as_view(), name='review-create'),
    path('reviews/update/<int:tutorid>/<int:pk>/', ReviewUpdateView.as_view(), name='review-update'),
    path('reviews/delete/<int:tutorid>/<int:pk>/', ReviewDeleteView.as_view(), name='review-delete'),

    path('reviews/new/<int:tutorid>/<int:sessionid>/', ReviewCreateViewWithId.as_view(), name='review-create-id')

  
]
