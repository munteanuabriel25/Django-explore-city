from .views import ListingDetailAPI, ListingListAPI
from django.urls import path, include


urlpatterns =[
    path('listings/', ListingListAPI, name='api-listing-all'),
    path('listings/<int:pk>/', ListingDetailAPI, name='api-detail'),

]