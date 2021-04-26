from PIL import Image
from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import reverse
from listing.models import Listing
from django.utils import timezone
from io import BytesIO
from django.core.files.base import ContentFile
from django.core.files import File


# Create your models here.
def user_media_path(instance, filename):
    return 'user_{0}/profile_pics/{1}'.format(instance.user.username, filename)


class PictureHandlerMixin:
    UserProfile = (300,300)
    
    def resize_image(self, image_field,model):
        """resize an picture to a given TUPLE dimensions"""
        if self._check_size(image_field,model):
            model = self.__getattribute__(model)
            im = Image.open(image_field)
            source_image = im.convert("RGB")
            source_image.thumbnail(model)
            output = BytesIO()
            source_image.save(output, format="JPEG")
            output.seek(0)
            content_file = ContentFile(output.read())
            file = File(content_file)
            image_field.save("{0}.jpeg".format(image_field.name.split(".")[0]), file, save=False)
        
    def _check_size(self, image_field, model):
        """check if an image size has propper dimensions for his purpose """
        model = self.__getattribute__(model)
        image = Image.open(image_field)
        if image.height > model[0] or image.width > model[1]:
            return True
        else:
            return False
    
    
    
class UserProfile(models.Model,PictureHandlerMixin):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    picture = models.ImageField(upload_to=user_media_path, default="default_prof_pic.jpg")
    facebook = models.CharField(max_length=200, blank=True, null=True)
    instagram = models.CharField(max_length=200, blank=True, null=True)
    blog_url = models.URLField(blank=True, null=True)
    description = models.CharField(max_length=250, blank=True)

    def save(self, *args, **kwargs):
        self.resize_image(self.picture, self.__class__.__name__) # check if the uploaded image by the user is not to big
        super(UserProfile,self).save(*args, **kwargs)
  
    @property
    def username(self):
        if self.name == None:
            return self.user.username
        else:
            return self.name

  
    def __str__(self):
        return "{} profile".format(self.user.username)
    
    def get_absolute_url(self):
        return reverse("pages:user:user-profile", args=[str(self.user.username)])