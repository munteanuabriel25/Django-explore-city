from django.contrib import admin
from django.urls import path, include
from . import views

# from this url patterns every request is redirected to specific app. If is not an app then calls the function form views.

app_name='pages'

urlpatterns = [
    path('', views.home_view, name="home-view",),
    path('listing/',include('listing.urls')),
    path('user/',include('user_profile.urls')),
    path('blog/',include('blog.urls')),

]
