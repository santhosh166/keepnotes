from time import *
from django.db import models
from django.db.models.deletion import CASCADE
from django.contrib.auth.models import User

# Create your models here.
class content(models.Model):
    
    user=models.ForeignKey(User,on_delete=CASCADE)
    title=models.CharField(max_length=200)
    description=models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return self.user.username+" Note"

