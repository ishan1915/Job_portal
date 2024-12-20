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


]