from django.db import models
from django.contrib.auth.models import User,AbstractUser
# Create your models here.

class UserDetail(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
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
    skills = models.ManyToManyField('Skill', blank=True)            
    

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
    mobile=models.CharField(max_length=12)
    email=models.EmailField(null=True)
    notice_period=models.CharField(max_length=10)

    applied_on=models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.candidate.username} - {self.job.title}"    
    




class ContactUs(models.Model):
    name=models.CharField(max_length=20)
    email=models.EmailField(null=True)
    phone=models.CharField(null=True,max_length=10)
    topic=models.TextField()

    def __str__(self):
        return f"{self.name} - {self.email} - {self.phone} S- {self.topic}"





class Company(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    website = models.URLField()
    address = models.TextField()
    description = models.TextField()
    logo = models.ImageField(upload_to='company_logos/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    


class Subject(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Question(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    question_text = models.TextField()
    option_a = models.CharField(max_length=200)
    option_b = models.CharField(max_length=200)
    option_c = models.CharField(max_length=200)
    option_d = models.CharField(max_length=200)
    correct_option = models.CharField(max_length=1, choices=[('A','A'),('B','B'),('C','C'),('D','D')])

class TestResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    score = models.IntegerField()
    correct_count = models.IntegerField()
    incorrect_count = models.IntegerField()
    taken_on = models.DateTimeField(auto_now_add=True)