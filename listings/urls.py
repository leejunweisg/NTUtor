from django.urls import path
from . import views
from listings import views as listing_views
from .views import home

urlpatterns = [
    path('', home, name='home'),
    path('listing/search/', listing_views.search, name='search'),
    path('listing/view/<int:pk>/', listing_views.ListingDetailView.as_view(), name='listing-detail'),
    path('listing/createListing/', listing_views.ListingCreateView.as_view(), name='listing-create'),
    path('listing/update/<int:pk>/', listing_views.ListingUpdateView.as_view(), name='listing-update'),
    path('listing/delete/<int:pk>/', listing_views.ListingDeleteView.as_view(), name='listing-delete'),  
]