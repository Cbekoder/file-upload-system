from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    picture = models.FileField(upload_to='profile_pics', default="default.png")
    phone = models.CharField(max_length=13, blank=True)
    organization = models.CharField(max_length=50, blank=True)
    address = models.CharField(max_length=50, blank=True)
    district = models.CharField(max_length=50, blank=True)
    region = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.username