from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User



# Create your models here.
class UserInfo(AbstractUser):
    phone = models.CharField(max_length=13)
    designation = models.CharField(max_length=50)
    branch = models.CharField(max_length=50)
    gender = models.CharField( max_length=50)

    
class Contact(models.Model):
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=13)
    email = models.CharField(max_length=50)
    content = models.TextField()
    timeStamp = models.DateTimeField(auto_now_add=True , blank = True)
    user = model.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return 'Message from '+ self.name
