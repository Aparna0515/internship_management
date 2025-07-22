from django.urls import path
from . views import *

urlpatterns=[
    # class based views
    
    path('list/',Internship_List.as_view(),name='list'),
    path('create/',Internship_Create.as_view(),name='create_internship'),
    path('detail/<int:pk>/',InternshipDetailView.as_view(),name='detail'),
    path('application_list/',ApplicationListView.as_view(),name='applications_list'),
    path('application_create/',ApplicationCreateView.as_view(),name='application_create'),
    # path('application_status/<int:pk>/',ApplicationStatusUpdateView.as_view(),name='application_status'),
    path('application_detail/',ApplicationDetailView.as_view(),name='application-detail'),

    # function based views
    path('resume/download/<int:pk>/',download_resume, name='download_resume'),
    path('application/<int:pk>/',view_application, name='view_application'),
    path('application/<int:pk>/<str:action>/',update_application_status,name='update_status')
]