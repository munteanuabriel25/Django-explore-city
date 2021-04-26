from django import template
from ..models import ListingCategory, Listing
from django.db.models import Count
register = template.Library()




@register.inclusion_tag("listing/sidebar_menu_category.html")
def sidebar_menu_category(active=None):
    """
    -get all Category Objects
    -set an attribute for each category listing
    -return active category
    """
    categories = ListingCategory.objects.annotate(no_listings=Count('listing_categ'))
    return {"categories": categories,
            "active_category":active }


