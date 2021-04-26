from django import template
from ..models import ListingCategory, Listing
from django.contrib.auth.models import User
register = template.Library()



@register.inclusion_tag("listing/wishlist_action_status.html")
def is_into_wishlist(listing, user):
    """this function check if an listing is allready into an user wishlist"""
    if user != None :
        if listing.wishlist.filter(id=user.id).exists():
            return {'answer': "yes",
                    'listing':listing}
        else:
            return {'answer':"no",
                    'listing':listing}

@register.inclusion_tag("pages/wishlist_profile_template_tags.html")
def populate_profile_wishlist(user):
    """this function check if an listing is allready into user wishlist"""
    if user != None :
        query= user.user_wishlist.all()
        return {'listings':query}


