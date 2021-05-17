from .views import ListingCategApiView, ListingDetailApiView, PostListingApiView, UserCreateApiView, UserLoginApiView
from django.urls import path, include


urlpatterns =[
    path('listings-categ/', ListingCategApiView.as_view(), name='api-listings-list'),
    path('listings-categ/<slug:categ_name>/', ListingCategApiView.as_view(), name='api-listing_categ-detail'),
    path('listings-categ/<slug:categ_name>/<int:pk>/', ListingDetailApiView.as_view(), name='api-listing-detail'),
    path('blog/', PostListingApiView.as_view(), name='api-post-list'),
    path('user/create/', UserCreateApiView.as_view(), name='api-user-create'),
    path('user/login/', UserLoginApiView.as_view(), name='api-user-login'),
    

]