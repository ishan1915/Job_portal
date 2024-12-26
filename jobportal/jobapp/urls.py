from django.urls import path
from . import views


urlpatterns = [
     
    
    # Authentication URLs
    path('signup/', views.signup, name='signup'),
    path('login/', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='user_logout'),

    path('admin_view',views.admin_view,name='admin_view'),
    path('admin_edit/<int:user_id>/',views.admin_edit,name='admin_edit'),


    path('candidate_view',views.candidate_view,name='candidate_view'),
    path('candidate_edit/<int:user_id>/',views.candidate_edit,name='candidate_edit'),


    path('resume_edit/',views.resume_edit,name='resume_edit'),
    path('resume_view/',views.resume_view,name='resume_view'),

    path('add_education/',views.add_education,name='add_education'),
    path('add_certification/',views.add_certificate,name='add_certification'),






]