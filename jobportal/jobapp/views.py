from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout
from .forms import SignupForm, LoginForm

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
    return redirect('home')

def admin_view(request):
    return render(request,'admin_view.html')

def candidate_view(request):
    return render(request,'candidate_view.html')