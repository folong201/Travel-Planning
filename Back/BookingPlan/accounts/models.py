from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class Accommodation(models.Model):
    ACCOMMODATION_TYPES = (
        ('hotel', 'Hotel'),
        ('apartment', 'Apartment'),
        ('villa', 'Villa'),
    )
    
    name = models.CharField(max_length=255)
    town = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    # description = models.TextField(max_length=255)
    image = models.ImageField(upload_to='images/accommodations/', null=True, blank=True)  
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2) 
    phone_number = models.CharField(max_length=15)
    type_of_accommodation = models.CharField(max_length=20, choices=ACCOMMODATION_TYPES)

    def __str__(self):
        return self.name


class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('accommodation_receptionist', 'Accommodation_Receptionist'),
        ('agency_receptionist', 'Agency_Receptionist'),
        ('client', 'Client'),
    ]
    roles = models.CharField(max_length=50, choices=ROLE_CHOICES, null=True, blank=True, default='client')


class Agency(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='image/agency/')
    description = models.TextField()
    
    agency_receptionist = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, 
        null=True, limit_choices_to={'roles': 'agency_receptionist'},related_name='managed_agencies'
    )

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
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
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    accommodation = models.ForeignKey(Accommodation, on_delete=models.CASCADE)
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'Booking by {self.user.username} for {self.accommodation.name}'



