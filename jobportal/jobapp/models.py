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
    profile_photo = models.ImageField(upload_to='profilephotos/', null=True, blank=True)



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
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    degree_name = models.CharField(max_length=100)
    university_name = models.CharField(max_length=100)
    year_of_passing = models.CharField(max_length=10)  
    marks_obtained = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.degree_name} - {self.university_name} ({self.year_of_passing})"
    

class Certification(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE) 
    certification_name=models.CharField(max_length=30)
    issued_by=models.CharField(max_length=50)
    issued_on=models.DateField(null=True)
    
    def __str__(self):
        return f"{self.certification_name}"



class Job(models.Model):
    company=models.ForeignKey(User,on_delete=models.CASCADE)
    title=models.CharField(max_length=20)
    description=models.TextField()
    location=models.CharField(max_length=20)
    posted_on=models.DateTimeField()
    closed_on=models.DateTimeField()

    def __str__(self):
        return self.title
    



class Application(models.Model):
    job=models.ForeignKey(Job,on_delete=models.CASCADE)
    candidate=models.ForeignKey(User,on_delete=models.CASCADE)
    name=models.CharField(max_length=100)#name as per govtid/certificate
    aadhar=models.CharField(max_length=12)
    applied_on=models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.candidate.username} - {self.job.title}"    