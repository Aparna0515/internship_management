from rest_framework import serializers
from .models import CustomUser,CompanyProfile,StudentProfile
from django.contrib.auth import authenticate
import re
class StudentRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model=CustomUser
        fields=['username','password','email']
        extra_kwargs={'password':{'write_only':True}}

    def create(self,validated_data):
        user=CustomUser.objects.create_user(**validated_data)
        user.is_student=True
        user.save()
        StudentProfile.objects.create(user=user,skills='',resume=None)
        return user
    
    def validate_email(self, value):
        email_regex = r'^[\w\.-]+@[\w\.-]+\.\w{2,4}$'
        if not re.match(email_regex, value):
            raise serializers.ValidationError("Enter a valid email address.")

        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")

        return value
    

class CompanyRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model=CustomUser
        fields=['username','password']
        extra_kwargs={'password':{'write_only':True}}

    def create(self,validated_data):
        user=CustomUser.objects.create_user(**validated_data)
        user.is_company=True
        user.save()
        CompanyProfile.objects.create(user=user, company_name='', website='')
        return user

class LoginSerializer(serializers.ModelSerializer):
    username=serializers.CharField()
    password=serializers.CharField()
    class Meta:
        model=CustomUser
        fields=['username','password']

    def validate(self, data):
        user=authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Invalid credentials")
    
class CompanyProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=CompanyProfile
        fields=['company_name','website']   

class StudentProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=StudentProfile
        fields=['skills','resume']  
        