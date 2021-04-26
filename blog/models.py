from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.shortcuts import reverse
from datetime import datetime
import pytz
from django.template.defaultfilters import slugify

# Create your models here.

def user_media_path(instance, filename):
    return 'user_{0}/posts_pics/{1}'.format(instance.user.username, filename)


class PostManager(models.Manager):
    pass



class Tag(models.Model):
    name = models.CharField(max_length=20)
    slug = models.SlugField(max_length=20, blank=False, unique=True)
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Tag, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
    
    
    
class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name="post_user")
    picture  = models.FileField(upload_to=user_media_path, blank=True)
    likes = models.ManyToManyField(User,blank=True)
    pub_date = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    content=models.TextField(null=False,blank=False)
    title = models.CharField(max_length=60,blank=False)
    wishlist = models.ManyToManyField(User, related_name="post_wishlist", blank=True)
    tags= models.ManyToManyField(Tag, related_name='posts', blank=True, null=True)
    # remove blank=true fro many to may  has no effect on it
    
    objects= PostManager()
    
    
    def __str__(self):
        return "{0.title} post written by {0.user.username}".format(self)

    def number_comments(self):
        return self.comment_set.all().count()
    
    def number_likes(self):
        return self.likes.all().count()
        
    def get_absolute_url(self):
        return reverse ('pages:blog:post_detail', kwargs={'post_id': self.pk})
    
    def get_action_url(self):
        return reverse('pages:blog:post_action', kwargs={'post_id': self.pk})
    
    def get_review_url(self):
        return reverse('pages:blog:post_review', kwargs={'post_id':self.pk})
    
    def get_comments(self):
        return self.comment_set.all().order_by('pub_date')
    
    def get_related(self):
        return self.user.post_user.filter(user=self.user)
    
    



class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
    pub_date = models.DateTimeField(auto_now_add=True)
    content = models.TextField(max_length=500, null=False)
    last_updated = models.DateTimeField(auto_now=True)
    
    def action_url(self):
        return reverse('pages:blog:comment_action',kwargs={'post_id': self.post.pk,'comment_id':self.pk })
    
    def time_since(self):
        datetimees = datetime(self.pub_date.year,self.pub_date.month, self.pub_date.day, self.pub_date.hour,self.pub_date.minute)
        
        return  datetimees.hour



        