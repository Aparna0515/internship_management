from django.shortcuts import render,redirect
from internships.models import Application,Internship
from users.models import StudentProfile,CompanyProfile
from django.contrib.auth.decorators import login_required
# Create your views here.

def home(request):
    return render(request,'base.html')


@login_required
def redirect_dashboard(request):
    if request.user.is_student:
        return redirect('student_dashboard')
    elif request.user.is_company:
        return redirect('company_dashboard')
    else:
        return redirect('login')  


@login_required
def student_dashboard(request):
    try:
        student = StudentProfile.objects.get(user=request.user)
        applications = Application.objects.select_related('internship__company').filter(student=student)
        return render(request, 'student_dashboard.html', {'applications': applications, 'student': student})
    except StudentProfile.DoesNotExist:
        return render(request, 'error.html', {'message': 'Student profile not found'})

# COMPANY DASHBOARD
@login_required
def company_dashboard(request):
    try:
        company = CompanyProfile.objects.get(user=request.user)
        internships = Internship.objects.prefetch_related('applications__student__user').filter(company=company)
        return render(request, 'company_dashboard.html', {'internships': internships, 'company': company})
    except CompanyProfile.DoesNotExist:
        return render(request, 'error.html', {'message': 'Company profile not found'})