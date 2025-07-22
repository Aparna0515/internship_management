from django.urls import path
from . import views
from internships.views import view_application
urlpatterns = [
    # path('',views.redirect_dashboard,name='redirect'),
    path('',views.home,name='home'),
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
    path('company/dashboard/', views.company_dashboard, name='company_dashboard'),

]
