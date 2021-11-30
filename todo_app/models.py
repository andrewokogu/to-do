from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()
# Create your models here.

class Todo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='to_do', null=True,blank=True)
    activity = models.CharField(max_length=350)
    completed =  models.BooleanField(default=False)
    date = models.DateField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return f'{self.activity} for {self.user.username}'
    
    
    def delete(self):
        self.is_active = False
        self.save()
        return

# from django.db import models
# from django.db import models
# from django.contrib.auth.models import User
# from django.utils import timezone
# from datetime import date, datetime

# # Create your models here.
# def getday():
#     date = timezone.now()
#     day = datetime.strftime(date, "%a-%d-%b-%y")
#     return(day)

# class Todo(models.Model):
#     # name=models.ForeignKey(User, on_delete=models, max_length=100)
#     name=models.CharField(max_length=20)
#     title=models.CharField(max_length=25)
#     body=models.TextField()
#     date = models.CharField(default=getday, max_length=50)
#     created_at = models.DateTimeField()

#     def __str__(self):
#         return self.name