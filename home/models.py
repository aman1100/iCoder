from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    firstName = models.CharField(max_length =50)
    lastName =models.CharField(max_length =50)
    username = models.CharField(max_length =50)
    phone = models.CharField(max_length=13)
    designation = models.CharField(max_length=50)
    branch = models.CharField(max_length=50)
    gender = models.CharField( max_length=50)
    
    def __str__(self):
        return self.username
    
    
    
class Contact(models.Model):
    sno = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=13)
    email = models.CharField(max_length=50)
    content = models.TextField()
    timeStamp = models.DateTimeField(auto_now_add=True , blank = True)

    def __str__(self):
        return 'Message from '+ self.name