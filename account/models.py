from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid
# Create your models here.

class CustomUser(AbstractUser):
# class User(AbstractUser):    
    id = models.UUIDField(primary_key=True, unique=True, editable=False, default=uuid.uuid4)
    # address = models.TextField(null=True, blank=True)
    # email = models.EmailField(max_length=30, null=True, blank=True)


    def __str__(self):
        return self.username