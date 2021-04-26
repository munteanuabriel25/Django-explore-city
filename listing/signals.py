from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Listing, Rating


@receiver(post_save, sender=Rating)
def update_listing_rating(sender, instance, **kwargs):
    # check wich listing rating has been modified
    listing = Listing.objects.get(id=instance.listing.id)
    # get the number of users who rated particular listing
    no_rates = Rating.objects.filter(listing=listing).count()
    total_score = 0
    query = Rating.objects.filter(listing=listing)
    for item in query:
        total_score += item.value
    # save the new value for listing rate score
    listing.rating = round(total_score / no_rates)
    listing.save()

