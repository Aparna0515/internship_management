from django.db import models
from users.models import CompanyProfile,StudentProfile
# Create your models here.
class Internship(models.Model):
    title=models.CharField(max_length=100)
    description=models.TextField()
    stipend=models.DecimalField(max_digits=10,decimal_places=2,blank=True,null=True,help_text='stipend amount')
    duration=models.CharField(max_length=100,help_text='eg. 3 months, 6 months')
    deadline=models.DateField(help_text='last date to apply')
    company=models.ForeignKey(CompanyProfile,on_delete=models.CASCADE,related_name='internships')

    class Meta:
        ordering=['-deadline']

    def __str__(self):
        return f"{self.title} at {self.company.company_name}"
    
class Application(models.Model):
    STATUS_CHOICES=[
        ('1','Applied'),
        ('2','Accepted'),
        ('3','Rejected'),
    ]
    student=models.ForeignKey(StudentProfile,on_delete=models.CASCADE,related_name='student_applications')
    internship=models.ForeignKey(Internship,on_delete=models.CASCADE,related_name='applications')
    status=models.IntegerField(max_length=15,choices=STATUS_CHOICES,default=1)
    applied_at=models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering=['-applied_at']
        unique_together=('student','internship')
    
    def __str__(self):
        return f"{self.student.user.username} applied for {self.internship.title}"
    
