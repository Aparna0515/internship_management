from .models import Internship,Application
from rest_framework import serializers
from datetime import date
class InternshipStudentSerializer(serializers.ModelSerializer):
    company_name=serializers.CharField(source='company.company_name',read_only=True)
    class Meta:
        model=Internship
        fields=['id','title','description','stipend','duration','deadline','company_name']
        read_only_fields=['id','title','description','stipend','duration','deadline','company_name']

class InternshipCompanySerializer(serializers.ModelSerializer):
    company_name=serializers.CharField(source='company.company_name',read_only=True)
   
    class Meta:
        model=Internship
        fields=['title','description','stipend','duration','deadline','company_name']


class ApplicationSerializer(serializers.ModelSerializer):
    internship_title=serializers.CharField(source='internship.title',read_only=True)
    company_name=serializers.CharField(source='internship.company.company_name',read_only=True)
    student=serializers.CharField(source='student.user.username',read_only=True)

    class Meta:
        model=Application
        fields=['student','internship','status','applied_at','internship_title','company_name']
        read_only_fields=['applied_at','student','status']

    def validate_internship(self,internship):
        if date.today()>internship.deadline:
            raise serializers.ValidationError("Deadline to apply for this internship is over")
        return internship
    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['student'] = request.user.student_profile
        validated_data['status']=1
        return super().create(validated_data)  
    
class ApplicationStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ['status']




        
