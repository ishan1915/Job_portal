from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from django.db.models import Q  
from django.contrib import messages
from django.contrib.auth import logout
from django.views import View
from .forms import SignupForm, LoginForm,UserDetailForm,ResumeForm,EducationForm,CertificationForm,JobForm,ApplicationForm,ContactForm,AdminLoginForm,CompanyRegistrationForm
from .models import UserDetail,Resume,Skill,Education,Certification,Job,Application,ContactUs,Company, Subject, Question, TestResult

from django.contrib.auth.decorators import user_passes_test
from django.contrib.admin.views.decorators import staff_member_required




def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)   
            return redirect('home')   
            
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})

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
                    return redirect('admin_view')   
                else:
                    return redirect('candidate_view')
            else:
                form.add_error(None, "Invalid login credentials.")
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})


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
            return redirect('admin_view')   
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
            return redirect('candidate_view')   
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
            return redirect('resume_view')   
        else:
            print(form.errors)  
    else:
        form = ResumeForm(instance=resume)

    return render(request, 'resume_edit.html', {'form': form})

 
def resume_view(request):
    try:
        resume = Resume.objects.get(user=request.user)
        existing_education = Education.objects.filter(user=request.user)

    except Resume.DoesNotExist:
        resume = None   

    return render(request, 'resume_view.html', {'resume': resume,'existing_education':existing_education})





def add_education(request):
    user = request.user
    existing_education = Education.objects.filter(user=user)

    if request.method == 'POST':
        form = EducationForm(request.POST, request.FILES)

        
        if form.is_valid():
            education = form.save(commit=False)
            education.user = user   
            education.save()
            return redirect('candidate_view')   
    else:
        form = EducationForm()

    
    return render(request, 'add_education.html', {'form': form, 'existing_education': existing_education})

def add_certificate(request):
    user = request.user
    
    existing_certificate = Certification.objects.filter(user=user)

    
    if request.method == 'POST':
         form = CertificationForm(request.POST, request.FILES)

         if form.is_valid():
            education = form.save(commit=False)
            education.user = user   
            education.save()
            return redirect('candidate_view')   
    else:
        
        form = CertificationForm()

    
    return render(request, 'add_certification.html', {'form': form, 'existing_certificate': existing_certificate})





 

# Create Job Posting (for companies)
@login_required
def post_job(request):
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.company = request.user  
            job.save()
            return redirect('job_list')  
    else:
        form = JobForm()

    return render(request, 'post_job.html', {'form': form})

# View Job Listings (for candidates)
def job_list(request):
    jobs = Job.objects.all()  
    return render(request, 'job_list.html', {'jobs': jobs})


@login_required
def apply_for_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    
    if request.user == job.company:
        return redirect('company_dashboard')  

    
    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.candidate = request.user
            application.save()

            
            return redirect('job_list')   

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
    edu = Education.objects.filter(user=application.candidate)
    cert = Certification.objects.filter(user=application.candidate)

    return render(request, 'candidate_details.html', {
        'application': application,
        'resume': resume,
        'edu':edu,
        'cert':cert
    })


 

# Search View
class JobSearchView(View):
    def get(self, request):
        query = request.GET.get('query', '')
        jobs = Job.objects.filter(closed_on__gt=now())

        if query:
            jobs = jobs.filter(Q(title__icontains=query) | Q(location__icontains=query) | Q(description__icontains=query))

        return render(request, 'search.html', {'jobs': jobs})



 
def home(request):
    return render(request, 'homepage.html')



def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            topic = form.cleaned_data['topic']

            ContactUs.objects.create(name=name, email=email, phone=phone,topic=topic)

            return render(request, 'success.html')

    else:
        form = ContactForm()

    return render(request, 'contact_form.html', {'form': form})



def admin_login_view(request):
    if request.method == 'POST':
        form = AdminLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None and user.is_superuser:
                login(request, user)
                return redirect('admin_dashboard')  # change to your admin dashboard URL name
            else:
                messages.error(request, 'You must be a superuser to log in.')
    else:
        form = AdminLoginForm()

    return render(request, 'admin_login.html', {'form': form})

@user_passes_test(lambda u: u.is_superuser)
def admin_dashboard(request):
    contacts = ContactUs.objects.all()
    return render(request, 'admin_dashboard.html', {'contacts': contacts})



def company_registration(request):
    if request.method == 'POST':
        form = CompanyRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()  # Save the company to the database
            return render(request, 'success.html')

    else:
         form = CompanyRegistrationForm()

    return render(request, 'company_registration.html', {'form': form})








@staff_member_required
def company_list(request):
    companies = Company.objects.all().order_by('-created_at')
    return render(request, 'company_list.html', {'companies': companies})




@login_required
def select_subject(request):
    subjects = Subject.objects.all()
    return render(request, 'select_subject.html', {'subjects': subjects})





@login_required
def start_test_page(request, subject_id):
    subject = get_object_or_404(Subject, pk=subject_id)
    return render(request, 'start_test.html', {'subject': subject})

@login_required
def start_test(request, subject_id):
    subject = get_object_or_404(Subject, pk=subject_id)
    questions = Question.objects.filter(subject=subject).order_by('?')[:30]
    request.session['question_ids'] = [q.id for q in questions]
    return render(request, 'test.html', {'subject': subject, 'questions': questions})

@login_required
def submit_test(request, subject_id):
    subject = get_object_or_404(Subject, pk=subject_id)
    question_ids = request.session.get('question_ids', [])
    questions = Question.objects.filter(id__in=question_ids)

    correct = 0
    total = questions.count()

    for q in questions:
        selected = request.POST.get(f'q{q.id}')
        if selected == q.correct_option:
            correct += 1

    incorrect = total - correct

    result = TestResult.objects.create(
        user=request.user,
        subject=subject,
        score=correct,
        correct_count=correct,
        incorrect_count=incorrect
    )

    return render(request, 'result.html', {
        'score': correct,
        'total': total,
        'correct_count': correct,
        'incorrect_count': incorrect
    })

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import Sort

class SortArray(APIView):
    def post(self, request):
        
        serializer = Sort(data=request.data)

        if serializer.is_valid():
            numbers = serializer.validated_data['numbers']
            sorted_numbers = sorted(numbers)

            return Response({"sorted_numbers":sorted_numbers})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)