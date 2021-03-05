from django.urls import path
from . import views
from listings import views as listing_views

urlpatterns = [
    path('', views.home, name='home'),
    path('listing/view/<int:pk>/', listing_views.ListingDetailView.as_view(), name='listing-detail'),
    path('listing/createListing/', listing_views.ListingCreateView.as_view(), name='listing-create'),
    path('listing/update/<int:pk>/', listing_views.ListingUpdateView.as_view(), name='listing-update'),
    path('listing/delete/<int:pk>/', listing_views.ListingDeleteView.as_view(), name='listing-delete'),
    path('refreshmodules1236172', views.refresh_modules, name='refresh-modules'), # do not go to this URL unnecessarily
]
