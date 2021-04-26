from django.urls import path
from . import views



app_name='user'

urlpatterns = [
    path('profile/<str:username>/', views.update_user_profile, name='user-profile'),
    path('login/', views.user_login_view, name='user-login'),
    path('logout/', views.user_logout_view, name='user-logout'),
    path('register/', views.user_register_view, name='user-register'),
    path('post_create/<str:username>/', views.new_post, name='post-create'),

]

