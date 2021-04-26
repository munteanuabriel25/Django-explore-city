from django import template
from ..models import Post
from django.contrib.auth.models import User
register = template.Library()


@register.inclusion_tag("blog/review_post_blog.html")
def check_status(post, user):
    """this function check if an user allready liked a post and added to wishlist """
    context={'post': post }
    
    if user != None :
        
        if post.likes.filter(username=user.username).exists():
            context["liked_it"] = "true"
        else:
            context["liked_it"] = "false"
            
        if post.wishlist.filter(username=user.username).exists():
            context["wished_it"] = "true"
        else:
            context["wished_it"] = "false"
 
    return context
