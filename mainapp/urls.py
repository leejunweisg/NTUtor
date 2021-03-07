from django.urls import path, include

from . import views
from reviews import views as review_views
from reviews.views import ReviewListView, ReviewCreateView, ReviewUpdateView, ReviewDeleteView


urlpatterns = [
    path('', views.home, name='home'),
    path('refreshmodules1236172', views.refresh_modules, name='refresh-modules'), # do not go to this URL unnecessarily
    path('',include('reviews.urls'))

    

]
