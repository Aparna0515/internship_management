from django.contrib import admin
from users.models import CustomUser, StudentProfile, CompanyProfile
from internships.models import Internship, Application

class MyAdminSite(admin.AdminSite):
    site_header = "InternManager Admin"
    site_title = "InternManager Admin Portal"
    index_title = "Welcome to InternManager Admin Dashboard"

    def index(self, request, extra_context=None):
        # Gather analytics data
        extra_context = extra_context or {}
        extra_context.update({
            'total_students': StudentProfile.objects.count(),
            'total_companies': CompanyProfile.objects.count(),
            'total_users': CustomUser.objects.count(),
            'total_internships': Internship.objects.count(),
            'total_applications': Application.objects.count(),
        })
        return super().index(request, extra_context=extra_context)

# Create instance
custom_admin_site = MyAdminSite(name='myadmin')

# Register your models with the custom admin site
custom_admin_site.register(CustomUser)
custom_admin_site.register(StudentProfile)
custom_admin_site.register(CompanyProfile)
custom_admin_site.register(Internship)
custom_admin_site.register(Application)
