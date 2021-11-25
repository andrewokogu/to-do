from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class CustomUser(AbstractUser):
    address = models.TextField(null=True, blank=True)
    email = models.EmailField(max_length=30, null=True, blank=True)