from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

# Create your models here.
class Listing(models.Model):
    Title = models.CharField(max_length=30, default='House on Sale')
    slug = models.CharField(max_length=100, null=True, blank=True)
    Location = models.CharField(max_length=30, default='Kalanki')
    City = models.CharField(max_length=30, default='Kathmandu')
    Price = models.IntegerField(default=9999999)
    Bedroom = models.IntegerField(default=1)
    Bathroom = models.IntegerField(default=1)
    Floors = models.IntegerField(default=1)
    Parking = models.IntegerField(default=1)
    Face = models.CharField(max_length=30, default="East")
    Area = models.IntegerField(default=100)
    Road_Width = models.IntegerField(default=0)
    Road_Type = models.CharField(max_length=30, default="Concrete")
    Build_Area = models.IntegerField(default=100)
    Amenities = models.CharField(max_length=30, default="Bathroom")
    Contact_number = models.IntegerField(default=9845654321)
    Contact_mail = models.EmailField(max_length=30, default='admin@gmail.com')
    Image = models.ImageField(max_length = 254)
    user = models.ForeignKey(User, on_delete=models.SET_NULL,null=True)
    is_sold = models.BooleanField(default=False)
    Description = models.CharField(max_length=1000, default="Please describe your estate here. You may also justify the price of your estate here.")
    likes = models.ManyToManyField(User, related_name='estate')

    def __str__(self):
        return self.Title
    
    def save(self, *args, **kwargs):
        if self.slug is None or self.slug!=slugify(self.Title):
            self.slug = slugify(self.Title)
        return super().save(*args, **kwargs)

class Comment(models.Model):
    listing = models.ForeignKey(Listing, related_name = "comments", on_delete = models.CASCADE)
    name = models.CharField(max_length=100, default="Anonymous User")
    body = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    # def sample_view(request):
    #     name = request.user

    def __str__(self):
        return '%s - %s' % (self.listing.Title, self.name)

class ListingImage(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='listing_images/')

    def __str__(self):
        return '%s - %s' % (self.listing.Title, 'images')