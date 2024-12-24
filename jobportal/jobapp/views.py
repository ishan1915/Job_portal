from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required

from django.contrib.auth import logout
from .forms import SignupForm, LoginForm,UserDetailForm,ResumeForm,EducationForm
from .models import UserDetail,Resume,Skill,Education

# User Signup (Registration) view
def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Automatically log the user in after signup
            return redirect('home')  # Redirect to home page
            
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})

# User Login view
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                if user.is_staff:
                    return redirect('admin_view')  # Redirect to home page
                else:
                    return redirect('candidate_view')
            else:
                form.add_error(None, "Invalid login credentials.")
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})

# User Logout view
def user_logout(request):
    logout(request)
    return redirect('user_login')

def admin_view(request):
    try:
        user_detail=UserDetail.objects.get(user=request.user)
    except  UserDetail.DoesNotExist:
        user_detail = None    
    return render(request,'admin_view.html',{'user_detail':user_detail})

def admin_edit(request,user_id):
    try:
        user_detail = UserDetail.objects.get(id=user_id,user=request.user)
    except UserDetail.DoesNotExist:
        user_detail = UserDetail(user=request.user)
    
    if request.method == 'POST':
        form = UserDetailForm(request.POST, request.FILES ,instance=user_detail)
        if form.is_valid():
            form.save()
            return redirect('admin_view')  # Redirect to profile view after editing
    else:
        form = UserDetailForm(instance=user_detail)
    
    return render(request, 'admin_edit.html', {'form': form})

def candidate_view(request):
    try:
        user_detail=UserDetail.objects.get(user=request.user)
    except  UserDetail.DoesNotExist:
        user_detail = None    
    return render(request,'candidate_view.html',{'user_detail':user_detail})



def candidate_edit(request,user_id):
    try:
        user_detail = UserDetail.objects.get(id=user_id,user=request.user)
    except UserDetail.DoesNotExist:
        user_detail = UserDetail(user=request.user)
    
    if request.method == 'POST':
        form = UserDetailForm(request.POST, request.FILES ,instance=user_detail)
        if form.is_valid():
            form.save()
            return redirect('candidate_view')  # Redirect to profile view after editing
    else:
        form = UserDetailForm(instance=user_detail)
    
    return render(request, 'candidate_edit.html', {'form': form})


def resume_edit(request):
    try:
        resume = Resume.objects.get(user=request.user)
    except Resume.DoesNotExist:
        resume = Resume(user=request.user)

    if request.method == 'POST':
        form = ResumeForm(request.POST, instance=resume)
        if form.is_valid():
            form.save()
            return redirect('resume_view')  # Redirect to a page that shows the resume after saving
        else:
            print(form.errors)  # To check any validation errors
    else:
        form = ResumeForm(instance=resume)

    return render(request, 'resume_edit.html', {'form': form})

 
def resume_view(request):
    try:
        resume = Resume.objects.get(user=request.user)
    except Resume.DoesNotExist:
        resume = None  # If the user doesn't have a resume yet, set resume to None

    return render(request, 'resume_view.html', {'resume': resume})





def add_education(request):
    # Get the logged-in user
    user = request.user
    
    # Check if there are any existing education records
    existing_education = Education.objects.filter(user=user)

    # If the form is submitted
    if request.method == 'POST':
        # Check if the user is editing an existing education record or adding a new one
        form = EducationForm(request.POST, request.FILES)

        # If the form is valid, save the education record
        if form.is_valid():
            education = form.save(commit=False)
            education.user = user  # Assign the logged-in user to the education record
            education.save()
            return redirect('candidate_view')  # Redirect to a page displaying all education records
    else:
        # If not a POST request, create an empty form for adding a new education record
        form = EducationForm()

    # Render the form
    return render(request, 'add_education.html', {'form': form, 'existing_education': existing_education})

