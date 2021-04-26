from django import template
from ..models import Listing
from django.db.models import Count
register = template.Library()




@register.inclusion_tag("listing/ordered_listing_rating.html")
def get_top_rated():
    """this template is used for top 5 rated listings"""
    top_rated = Listing.objects.get_top_rated()

    return {"top_rated": top_rated,
            "name": "TOP RATED LISTINGS"}

@register.inclusion_tag("listing/ordered_listing_added.html")
def get_lasted_added():
    """this template is used for latest 5 added listings"""
    latest_added = Listing.objects.get_last_posted()
    return {"top_added": latest_added,
            "name": "LATEST ADDED LISTINGS"}

