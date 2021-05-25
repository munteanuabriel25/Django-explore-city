from django.shortcuts import render, get_object_or_404
from .models import Listing, ListingCategory, Rating
from django.views.generic import View
from django.core.paginator import Paginator, PageNotAnInteger,EmptyPage
from django.contrib.auth.decorators import login_required

from django.http import HttpResponseRedirect
# Create your views here.



class CategoryListing(View):
    template_name= 'listing/base_listing.html'
    context= ''
    paginate_by=12
    page_kwarg='page'
    
    def get(self, request, category_name_slug):
        category = get_object_or_404(ListingCategory, slug__iexact=category_name_slug)
        listings= Listing.objects.filter(category_id=category_name_slug)
        paginator = Paginator(listings,self.paginate_by)
        page_number = request.GET.get(self.page_kwarg)
        try:
            page = paginator.page(page_number)
        except PageNotAnInteger:
            page =paginator.page(1)
        except EmptyPage:
            page = paginator.page(paginator.num_pages)
            
        if page.has_previous():
            previous_url =  "?{pkw}={n}".format(pkw=self.page_kwarg, n=page.previous_page_number())
        else:
            previous_url= None
            
        if page.has_next():
            next_url = "?{pkw}={n}".format(pkw=self.page_kwarg, n=page.next_page_number())
        else:
            next_url= None
      
        context= {
            'category':category,
            'listings':page,
            'is_paginated': page.has_other_pages(),
            'previous_url': previous_url,
            'next_url': next_url,
        }
        return render(request, self.template_name, context)
    
    
    
# @login_required()
class WishlistAction(View):
    
    def post(self,request, listing_id):
        listing = get_object_or_404(Listing, id=listing_id)
        if listing.wishlist.filter(id=request.user.id).exists():
            listing.wishlist.remove(request.user)
        else:
            listing.wishlist.add(request.user)
    


def rating_action(request, listing_id):
    if request.user.is_authenticated:
        if request.method == "POST":
            # check if user allready rated this post
            value = int(request.POST.get('stars'))
            statement = Rating.objects.filter(user=request.user.id, listing=listing_id).exists()
            
            if statement:
                # if it is rated, change rating value with his new rating value
                rating_obj = Rating.objects.get(user=request.user.id, listing=listing_id)
                rating_obj.value = value
                rating_obj.save()
                # messages.success(request, 'Your rating was changed')
                return HttpResponseRedirect(request.META["HTTP_REFERER"])
            else:
                # if is not rated yet, set a rating for this listing
                listing_obj = Listing.objects.get(id=listing_id)
                rating_obj = Rating(user=request.user, value=value, listing=listing_obj)
                rating_obj.save()
                # messages.success(request, 'Your rating was changed')
                return HttpResponseRedirect(request.META["HTTP_REFERER"])
    else:
        # messages.success(request, "You have to log in in order to perform this action")
        return HttpResponseRedirect(request.META["HTTP_REFERER"])