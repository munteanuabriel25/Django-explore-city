from django import template
from ..models import Post, Tag
from django.db.models import Count
from django.contrib.auth.models import User
register = template.Library()

@register.inclusion_tag("blog/left_sidebar_blog.html")
def left_sidebar_blog():
    """from here get top 3 latest posts, top 3 travelers"""
    latest_posts = Post.objects.order_by('-pub_date')[0:3]
    top_storytellers = User.objects.annotate(num_posts=Count('post_user')).order_by('-num_posts')
    tags= Tag.objects.all()
    return {'latest_posts':latest_posts,
            'top_storytellers': top_storytellers,
            'tags': tags,
    }
    
    
    
    