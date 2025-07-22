from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class CustomUser(AbstractUser):
    phone=models.CharField(max_length=15)
    is_student = models.BooleanField(default=False)
    is_company = models.BooleanField(default=False)

class StudentProfile(models.Model):
    user=models.OneToOneField(CustomUser,on_delete=models.CASCADE,related_name='student_profile')
    skills=models.TextField(help_text='comma-seperated list of skills',blank=True)
    resume=models.FileField(upload_to='media/resumes/',blank=True,null=True)

    def __str__(self):
        return self.user.username

class CompanyProfile(models.Model):
    user=models.OneToOneField(CustomUser,on_delete=models.CASCADE,related_name='company_profile')
    company_name=models.CharField(max_length=100)
    website=models.URLField(blank=True,null=True)

    def __str__(self):
        return self.company_name
    
