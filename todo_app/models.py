from django.db import models
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import date, datetime

# Create your models here.
def getday():
    date = timezone.now()
    day = datetime.strftime(date, "%a-%d-%b-%y")
    return(day)

class Todo(models.Model):
    # name=models.ForeignKey(User, on_delete=models, max_length=100)
    name=models.CharField(max_length=20)
    title=models.CharField(max_length=25)
    body=models.TextField()
    date = models.CharField(default=getday, max_length=50)
    created_at = models.DateTimeField()

    def __str__(self):
        return self.name