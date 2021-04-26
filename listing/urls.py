from django.contrib import admin
from django.urls import path
from . import views

app_name='listing'

urlpatterns = [
    path('<str:category_name_slug>/', views.CategoryListing.as_view(), name="category-listing"),
    path('wishlist/<int:listing_id>/', views.WishlistAction.as_view(), name="wishlist-action"),
    path('rating/<int:listing_id>/', views.rating_action, name="rating-action"),
    
]



# inplement a home view for listing page with most rated views and payed listings