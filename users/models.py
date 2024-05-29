from django.db import models
from django.contrib.auth.models import AbstractUser

class Role(models.Model):
    title = models.CharField(max_length=50)
    def __str__(self):
        return self.title

class User(AbstractUser):
    picture = models.FileField(upload_to='profile_pics', default="default.png")
    phone = models.CharField(max_length=13, blank=True)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.username
