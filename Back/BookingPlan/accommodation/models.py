from django.db import models
from django.contrib.auth.models import User
from accounts.models import Accommodation  

class Receptionist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    accommodations = models.ManyToManyField(Accommodation, related_name='receptionists')

    def __str__(self):
        return f"Receptionist: {self.user.username}"
