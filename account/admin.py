from django.contrib import admin
from .models import CustomUser


# Register your models here.
# User = get_user_model()

admin.site.register(CustomUser)
