from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from .models import UserDetail,Skill,Resume,Education,Certification
from django.forms import modelformset_factory


class SignupForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username','email','password1','password2']


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Username')
    password = forms.CharField(widget=forms.PasswordInput)

class UserDetailForm(forms.ModelForm):
    class Meta:
        model = UserDetail
        fields = ['firstname', 'lastname', 'contact', 'email','address',]



class ResumeForm(forms.ModelForm):
    skills = forms.ModelMultipleChoiceField(
        queryset=Skill.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,  # Optional: Set to True if skills are required
    )
    
    class Meta:
        model = Resume
        fields = ['name', 'contact', 'email', 'address', 'skills']      


class EducationForm(forms.ModelForm):
    class Meta:
        model = Education
        fields = ['degree_name', 'university_name', 'year_of_passing', 'marks_obtained']
        
    def __init__(self, *args, **kwargs):
        super(EducationForm, self).__init__(*args, **kwargs)      


class CertificationForm(forms.ModelForm):
    class Meta:
        model = Certification
        fields = ['certification_name','issued_by','issued_on']
