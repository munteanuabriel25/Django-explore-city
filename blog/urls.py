from django.contrib import admin
from django.urls import path, include
from . import views

# from this url patterns every request is redirected to specific app. If is not an app then calls the function form views.

app_name='blog'

urlpatterns = [
    path('', views.HomeBlog.as_view(), name="home-view"),
    path('post/<int:post_id>', views.post_detail, name="post_detail"),
    path('post-comment-actions/', views.PostCommentActions.as_view(), name="comment_action"),
    # path('post-comment/<int:post_id>/<int:comment_id>/', views.CommentAction.as_view(), name="comment_action"),
    path('post-update/<int:post_id>/', views.UpdatePost.as_view(), name='post_action'),
    # path('post-review/<int:post_id>/', views.ReviewPost.as_view(), name='post_review'),
    path('post-review/', views.ReviewPost.as_view(), name='post_review'),

    
]
