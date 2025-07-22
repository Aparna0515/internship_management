from django.urls import path
from . views import *
urlpatterns=[
    # Company APIs
    path('company/register/',CompanyRegisterView.as_view(),name='register'),
    path('company/',CompanyProfileList.as_view(),name='company-list'),
    path('company_detail/<int:pk>/',CompanyProfileDetail.as_view(),name='company-detail'),
    
    # Student APIs
    path('student/register/',StudentRegisterView.as_view(),name='student-register'),
    path('student/',StudentProfileList.as_view(),name='student-list'),
    path('student_detail/<int:pk>/',StudentProfileDetail.as_view(),name='student-detail'),
    
    # Admin APIs
    path('admin/analytics/',AdminAnalyticsView.as_view(),name='admin-analytics'),    
    
    # function-based views 
    path('login/',  user_login, name='login'),
    path('logout/',user_logout,name='logout')
]