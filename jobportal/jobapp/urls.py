from django.urls import path
from . import views
from .views import JobSearchView


urlpatterns = [
     
    
    # Authentication URLs
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='user_logout'),

    path('search/', JobSearchView.as_view(), name='job_search'),

    path('admin_view',views.admin_view,name='admin_view'),
    path('admin_edit/<int:user_id>/',views.admin_edit,name='admin_edit'),


    path('candidate_view',views.candidate_view,name='candidate_view'),
    path('candidate_edit/<int:user_id>/',views.candidate_edit,name='candidate_edit'),


    path('resume_edit/',views.resume_edit,name='resume_edit'),
    path('resume_view/',views.resume_view,name='resume_view'),

    path('add_education/',views.add_education,name='add_education'),
    path('add_certification/',views.add_certificate,name='add_certification'),


    path('post_job/', views.post_job, name='post_job'),
    path('job_list/', views.job_list, name='job_list'),
    path('apply/<int:job_id>/', views.apply_for_job, name='apply_for_job'),
    path('company_dashboard/', views.company_dashboard, name='company_dashboard'),
    path('job/<int:job_id>/applicants/', views.job_applicants, name='job_applicants'),
    path('application/<int:application_id>/details/', views.candidate_details, name='candidate_details'),
    
    path('contact/', views.contact_view, name='contact'),
    path('adminlogin/', views.admin_login_view, name='admin_login'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),

    path('company-register/', views.company_registration, name='company_register'),
    path('registered-companies/', views.company_list, name='company_list'),







]