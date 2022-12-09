from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Listing(models.Model):
    Title = models.CharField(max_length=30, default='House on Sale')
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
    # Description = models.CharField(max_length=200, default="Please describe your estate here. You may also justify the price of your estate here.")

    def __str__(self):
        return self.Title