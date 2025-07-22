from django.shortcuts import render,get_object_or_404,redirect

from internships.models import Application, Internship
from .models import CustomUser,StudentProfile,CompanyProfile
from .serializers import StudentRegisterSerializer,LoginSerializer,CompanyRegisterSerializer,CompanyProfileSerializer,StudentProfileSerializer
from rest_framework import status,permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth import authenticate, login
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.pagination import PageNumberPagination

# Create your views here.
class StudentRegisterView(APIView):
    def post(self,request):
        try:
            serializer=StudentRegisterSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Student registered successfully'},status=status.HTTP_200_OK)
            return Response(serializer.errors,status=400)
        except Exception as e:
            return Response({'error':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
class CompanyRegisterView(APIView):
    def post(self,request):
        try:
            serializer=CompanyRegisterSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Company registered successfully'},status=status.HTTP_200_OK)
            return Response(serializer.errors,status=400)
        except Exception as e:
            return Response({'error':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
def user_login(request):
    try:
        if request.method == "POST":
            username = request.POST.get("username")
            password = request.POST.get("password")

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)

                # Only generate token if user is valid
                refresh = RefreshToken.for_user(user)
                token_data = {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
                print(token_data)

                if user.is_student:
                    return redirect("student_dashboard")
                elif user.is_company:
                    return redirect("company_dashboard")
                else:
                    return redirect("home")  # fallback if role is unknown
            else:
                return render(request, "login.html", {"error": "Invalid username or password"})

        # If not POST, just show the login page
        return render(request, "login.html")

    except Exception as e:
        # Always return a response even on error
        return render(request, "login.html", {"error": f"Login error: {str(e)}"})


def user_logout(request):
    logout(request)
    return redirect("login")

        
# class LoginView(APIView):
#     def post(self,request):
#         try:
#             serializer=LoginSerializer(data=request.data)
#             if serializer.is_valid():
#                 user=serializer.validated_data
#                 refresh = RefreshToken.for_user(user)
#                 token_data = {
#                     'refresh': str(refresh),
#                     'access': str(refresh.access_token),
#                 }
#                 if user.is_student:
#                     return redirect('student_dashboard')
#                 elif user.is_company:
#                     return redirect('company_dashboard')
                 
#                 return Response(token_data, status=status.HTTP_200_OK)
#             return Response(serializer.errors,status=400)
#         except Exception as e:
#             return Response({'error':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
class CompanyProfileList(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        try:
            company_profiles=CompanyProfile.objects.all()
            paginator=PageNumberPagination()
            paginator.page_size = 3
            company_profiles = paginator.paginate_queryset(company_profiles, request)
            serializer=CompanyProfileSerializer(company_profiles,many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({'error':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        
class CompanyProfileDetail(APIView):
    permission_classes=[IsAuthenticated]

    def get(self,request,pk):
        try:
            company=get_object_or_404(CompanyProfile,pk=pk)
            if not request.user.is_company or company.user!=request.user:
                return Response({'error': 'You are not authorized to view this company profile.'}, status=status.HTTP_403_FORBIDDEN)
            serializer=CompanyProfileSerializer(company)
            return Response(serializer.data)
        except Exception as e:
            return Response({'error':str(e)},status=status.HTTP_200_OK)
    def put(self,request,pk):
        
        try:
            company=get_object_or_404(CompanyProfile,pk=pk)
            if not request.user.is_company or company.user!=request.user:
                return Response({'error': 'You are not authorized to view this company profile.'}, status=status.HTTP_403_FORBIDDEN)
            serializer=CompanyProfileSerializer(company,request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,status=status.HTTP_200_OK)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    def delete(self,request,pk):
        
        try:
            company=get_object_or_404(CompanyProfile,pk=pk)
            if not request.user.is_company or company.user!=request.user:
                return Response({'error': 'You are not authorized to view this company profile.'}, status=status.HTTP_403_FORBIDDEN)
            company.delete()
            return Response({'message':'Deleted successfully'},status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({'error':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class StudentProfileList(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        try:
            students=StudentProfile.objects.all()
            paginator=PageNumberPagination()
            paginator.page_size = 3 
            students = paginator.paginate_queryset(students, request)
            serializer=StudentProfileSerializer(students,many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class StudentProfileDetail(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request,pk):
        
        try:
            student=get_object_or_404(StudentProfile,pk=pk)
            if not request.user.is_student or student.user!=request.user:
                return Response({'error': 'You are not authorized to view this student profile.'}, status=status.HTTP_403_FORBIDDEN)
            serializer=StudentProfileSerializer(student)
            return Response(serializer.data)
        except Exception as e:
            return Response({'error':str(e)},status=status.HTTP_200_OK)
    def put(self,request,pk):
        
        try:
            student=get_object_or_404(StudentProfile,pk=pk)
            if not request.user.is_student or student.user!=request.user:
                return Response({'error': 'You are not authorized to view this student profile.'}, status=status.HTTP_403_FORBIDDEN)
            serializer=StudentProfileSerializer(student,request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,status=status.HTTP_200_OK)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    def delete(self,request,pk):
        
        try:
            student=get_object_or_404(StudentProfile,pk=pk)
            if not request.user.is_student or student.user!=request.user:
                return Response({'error': 'You are not authorized to view this student profile.'}, status=status.HTTP_403_FORBIDDEN)
            student.delete()
            return Response({'message':'Deleted successfully'},status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({'error':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class AdminAnalyticsView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        try:
            total_students = StudentProfile.objects.count()
            total_companies = CompanyProfile.objects.count()
            total_users = CustomUser.objects.count()
            total_internships = Internship.objects.count()
            total_applications = Application.objects.count()

            data = {
                'total_students': total_students,
                'total_companies': total_companies,
                'total_users': total_users,
                'total_internships': total_internships,
                'total_applications': total_applications
            }
            print(data)
            return render(request, 'admin/index.html', {'data': data})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
        