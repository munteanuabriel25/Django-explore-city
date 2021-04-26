from django.db import models
from django.template.defaultfilters import slugify
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


# Create your models here.


def user_media_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.user.username, filename)

class ListingManager(models.Manager):
    """ define custom queries for Listings"""
    
    def get_top_rated(self):
        """top 5 based by users rating"""
        return self.order_by('-rating')[:5]
    
    def get_last_posted(self):
        """top 5 based by users rating"""
        return self.order_by('-pub_date')[:5]


class ListingCategory(models.Model):
    name = models.CharField(unique=True, max_length=30)
    slug = models.SlugField(unique=True, primary_key=True)
    likes = models.IntegerField(default=0)
    icon = models.FileField(upload_to='listing_icon/',blank=True, null=True)
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(ListingCategory, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("pages:listing:category-listing", args=[self.slug])


class Listing(models.Model):
    category = models.ForeignKey(ListingCategory, on_delete=models.CASCADE,related_name="listing_categ" )
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    content = models.TextField(null=True)
    name = models.CharField(max_length=40, unique=True)
    address = models.CharField(max_length=40)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    picture = models.FileField(upload_to=user_media_path)
    rating = models.FloatField(default=0)
    pub_date = models.DateTimeField(auto_now_add=True)
    wishlist = models.ManyToManyField(User, related_name="user_wishlist", blank=True)
    
    objects=ListingManager()
    
    def __str__(self):
        return self.name
    
    # def get_absolute_url(self):
    #     return reverse("listing:show-listing", args=[self.category_id, self.id])
    
    class Meta:
        ordering =['name']

class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="rated by", null=True, blank=True)
    value = models.IntegerField()
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='listing_rating', null=True)
    rated = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.user.username + " rating for " + self.listing.name




# Create your models here.
