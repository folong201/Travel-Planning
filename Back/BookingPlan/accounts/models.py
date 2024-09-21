from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    address = models.CharField(max_length=255)
    travel_preferences = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='images/profile_pics/', null=True, blank=True)

    def __str__(self):
        return self.full_name

class Destination(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    city = models.CharField(max_length=100)
    popular_attractions = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='images/destination_img/', null= False, blank= False)

    def __str__(self):
        return f'{self.city}'

class Accommodation(models.Model):
    ACCOMMODATION_TYPES = (
        ('hotel', 'Hotel'),
        ('apartment', 'Apartment'),
        ('villa', 'Villa'),
    )
    
    name = models.CharField(max_length=255)
    town = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    image = models.ImageField(upload_to='images/accommodations/', null=True, blank=True)  
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2) 
    phone_number = models.CharField(max_length=15)
    type_of_accommodation = models.CharField(max_length=20, choices=ACCOMMODATION_TYPES)

    def __str__(self):
        return self.name

class Hotel(Accommodation):
    ROOM_TYPE_CHOICES = [
        ('Single', 'Single'),
        ('Double', 'Double'),
        ('Suite', 'Suite'),
    ]

    room_type = models.CharField(max_length=50, choices=ROOM_TYPE_CHOICES)

    def __str__(self):
        return f"{self.name} - {self.room_type}"


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    accommodation = models.ForeignKey(Accommodation, on_delete=models.CASCADE)
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'Booking by {self.user.username} for {self.accommodation.name}'


class Agency(models.Model):    
    name = models.CharField(max_length=255)
    location = models.TextField(max_length=255)
    image = models.ImageField(upload_to='images/agency/', null=True, blank=True)  
    simple_price = models.DecimalField(max_digits=10, decimal_places=2) 
    classic_price = models.DecimalField(max_digits=10, decimal_places=2) 
    vip_price = models.DecimalField(max_digits=10, decimal_places=2) 

    def __str__(self):
        return self.name



