from django.db import models
from django.contrib.auth.models import User,AbstractUser
# Create your models here.

class UserDetail(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    firstname=models.CharField(max_length=100)
    lastname=models.CharField(max_length=100)
    contact=models.CharField(max_length=20)
    email=models.EmailField(null=True)
    address=models.TextField(null=True)


    def __str__(self):
        return f"{self.user.username}'s details"
