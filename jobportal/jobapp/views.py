from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from django.db.models import Q  


from django.contrib.auth import logout
from django.views import View
from .forms import SignupForm, LoginForm,UserDetailForm,ResumeForm,EducationForm,CertificationForm,JobForm,ApplicationForm
from .models import UserDetail,Resume,Skill,Education,Certification,Job,Application

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
        existing_education = Education.objects.filter(user=request.user)

    except Resume.DoesNotExist:
        resume = None  # If the user doesn't have a resume yet, set resume to None

    return render(request, 'resume_view.html', {'resume': resume,'existing_education':existing_education})





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

def add_certificate(request):
    user = request.user
    
    existing_certificate = Certification.objects.filter(user=user)

    
    if request.method == 'POST':
         form = CertificationForm(request.POST, request.FILES)

         if form.is_valid():
            education = form.save(commit=False)
            education.user = user  # Assign the logged-in user to the education record
            education.save()
            return redirect('candidate_view')  # Redirect to a page displaying all education records
    else:
        # If not a POST request, create an empty form for adding a new education record
        form = CertificationForm()

    # Render the form
    return render(request, 'add_certification.html', {'form': form, 'existing_certificate': existing_certificate})





 

# Create Job Posting (for companies)
@login_required
def post_job(request):
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.company = request.user  # The logged-in company posts the job
            job.save()
            return redirect('job_list')  # Redirect to the job listing page
    else:
        form = JobForm()

    return render(request, 'post_job.html', {'form': form})

# View Job Listings (for candidates)
def job_list(request):
    jobs = Job.objects.all()  # Get all jobs
    return render(request, 'job_list.html', {'jobs': jobs})

# Apply for Job (for candidates)
@login_required
def apply_for_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    # Check if the user is not the company posting the job
    if request.user == job.company:
        return redirect('company_dashboard')  # Prevent company from applying to their own job

    # Handle form submission
    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            # Create the application object and assign the job and candidate fields
            application = form.save(commit=False)
            application.job = job
            application.candidate = request.user
            application.save()

            # Redirect to a success page or back to job listings
            return redirect('job_list')  # Change this URL name if needed

    else:
        form = ApplicationForm()

    return render(request, 'apply_for_job.html', {'form': form, 'job': job})

# Company View (to view applicants)
@login_required
def company_dashboard(request):
    jobs = Job.objects.filter(company=request.user)  
    
     
    

    return render(request, 'company_dashboard.html', {
        'jobs': jobs
         
    })



 

def job_applicants(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    applications = Application.objects.filter(job=job)

    return render(request, 'job_applicants.html', {
        'job': job,
        'applications': applications,
    })



def candidate_details(request, application_id):
    application = get_object_or_404(Application, id=application_id)
    resume = get_object_or_404(Resume, user=application.candidate)

    return render(request, 'candidate_details.html', {
        'application': application,
        'resume': resume,
    })


 

# Search View
class JobSearchView(View):
    def get(self, request):
        query = request.GET.get('query', '')
        jobs = Job.objects.filter(closed_on__gt=now())

        if query:
            jobs = jobs.filter(Q(title__icontains=query) | Q(location__icontains=query) | Q(description__icontains=query))

        return render(request, 'search.html', {'jobs': jobs})
