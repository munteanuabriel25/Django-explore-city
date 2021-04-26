from django import template
from ..models import ListingCategory, Listing,Rating
from django.contrib.auth.models import User

register = template.Library()



@register.inclusion_tag("listing/rating_action_status.html")
def color_rating_stars(listing, user):
    """this function colors the rating stars according to user previous rate """
    if user != None :
        # check if user is loged in and can rate a listing, return TRUE or FALSE
        rated = Rating.objects.filter(user=user.id, listing=listing.id).exists()
        if rated:
            rating = Rating.objects.get(user=user.id, listing=listing.id)
            star_list =[{"fill": 0, 'value':1},{"fill": 0, 'value':2},{"fill": 0, 'value':3},{"fill": 0, 'value':4},{"fill": 0, 'value':5}]
            
            # user allready rated this listing. Send the number of stars that user rated
            for i in range(rating.value):
                star_list[i]['fill']=1
                
            return {'rated': "yes",
                    'listing': listing,
                    'star_list':star_list
                    }
    
        else:
            # user does not rated this listing. The HTML template will handle this situation
            return {'rated':"no",
                    'listing':listing}
        
