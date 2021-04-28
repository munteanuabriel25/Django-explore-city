from django.urls import path
from . import views



app_name='user'

urlpatterns = [
    path('profile/<str:username>/', views.update_user_profile, name='user-profile'),
    path('login/', views.user_login_view, name='user-login'),
    path('logout/', views.user_logout_view, name='user-logout'),
    path('register/', views.UserRegisterView.as_view(), name='user-register'),
    path('activate/<uidb64>/<token>', views.activate_account, name='activate-account'),
    path('post_create/<str:username>/', views.new_post, name='post-create'),
    path('test/', views.test, name='test'),

]

