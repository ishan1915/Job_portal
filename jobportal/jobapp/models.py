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


class Skill(models.Model):
    name=models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Resume(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    name=models.CharField(max_length=20)
    contact=models.CharField(max_length=10)
    email=models.EmailField(max_length=20,blank=True)
    address=models.CharField(max_length=100)
    skills = models.ManyToManyField('Skill', blank=True)            # Many to many relationship with Skill
    

    def __str__(self):
        return f"{self.user.username}'s Resume"


class Education(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    degree_name = models.CharField(max_length=100)
    university_name = models.CharField(max_length=100)
    year_of_passing = models.CharField(max_length=10)  # You can make this a DateField if needed
    marks_obtained = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.degree_name} - {self.university_name} ({self.year_of_passing})"