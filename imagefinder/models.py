from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class User(AbstractUser):
    about = models.TextField(null=True)
    # image = models.ImageField(upload_to='profile_images',
    #                           default="http://www.mygolfkaki.com/DesktopModules/Custom%20Module/Member%20Management/Image/default.gif",
    #                           blank=True, null=True)

class TimeStampedModel(models.Model):
    created = models.DateField(auto_now_add=True)
    modified = models.DateField(auto_now=True)
    # Define as abstract base class
    # Therefore, no imagefinder_timestampedmodel table would be made
    class Meta:
        abstract = True


class Tag(TimeStampedModel):
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name


# Uniques are mapped by Page URL
class Image(TimeStampedModel):

    apiURL = models.CharField(max_length=200, null=True)
    api_id = models.IntegerField(null=True)
    title = models.CharField(max_length=150, null=True)
    author = models.CharField(max_length=100, null=True)
    pageURL = models.URLField()
    imageURL = models.URLField()
    thumbnailURL = models.URLField(null=True)
    favorites = models.ManyToManyField(User, blank=True, null=True, related_name='image') #hidden
    tags = models.ManyToManyField(Tag, blank=True, null=True, related_name='image')

    referrer = models.CharField(max_length=50, null=True)
    image = models.ImageField(upload_to='uploaded_images',
                               blank=True, null=True)

    def __unicode__(self):
        return unicode(self.pageURL)
