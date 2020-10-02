from django.db import models
from django.conf import settings
# Create your models here.

class Profile(models.Model):
    user=models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    nickname=models.CharField(max_length=20)
    profile_photo=models.ImageField(blank=True)