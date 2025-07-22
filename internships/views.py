from django.shortcuts import render,get_object_or_404,redirect
from . models import Internship,Application
from rest_framework.views import APIView
from .serializers import InternshipStudentSerializer,ApplicationSerializer,InternshipCompanySerializer,ApplicationStatusUpdateSerializer
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from django.conf import settings
from users.models import StudentProfile,CompanyProfile
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.decorators import login_required
from django.http import FileResponse, Http404
from django.conf import settings
from datetime import date
from rest_framework.pagination import PageNumberPagination
# Create your views here.
class Internship_List(APIView):
        permission_classes=[IsAuthenticated]

        def get(self,request):

            try:
                user=request.user
                internships=Internship.objects.all()

                if hasattr(user,'company_profile'):
                    internships=internships.filter(company=user.company_profile)
                elif hasattr(user,'student_profile'):
                    internships=internships.filter(deadline__gte=date.today())

                company=request.query_params.get('company')
                keyword=request.query_params.get('keyword')
                stipend=request.query_params.get('stipend')
                if company:
                    internships=internships.filter(company__company_name__icontains=company)
                if keyword:
                    internships=internships.filter(title__icontains='keyword')
                if stipend:
                    internships=internships.filter(stipend__gte='stipend')
                paginator = PageNumberPagination()
                paginator.page_size = 3  
                result_page = paginator.paginate_queryset(internships, request)

                serializer = InternshipStudentSerializer(result_page, many=True, context={'request': request})
                return paginator.get_paginated_response(serializer.data)
            except Exception as e:
                return Response({'error':str(e)},status=status.HTTP_400_BAD_REQUEST)
            
class Internship_Create(APIView):
        permission_classes=[IsAuthenticated]
        
        def post(self,request):
            if not request.user.is_company:
                return Response({'error': 'You are not authorized to perform this action.'}, status=status.HTTP_403_FORBIDDEN)
            try:
                serializer=InternshipCompanySerializer(data=request.data)
                if serializer.is_valid():
                    company_profile=request.user.company_profile
                    print(serializer.validated_data)
                    serializer.save(company=company_profile)
                    return Response(serializer.data,status=status.HTTP_201_CREATED)
                return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({'error':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class InternshipDetailView(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request,pk):
        try:
            internship=get_object_or_404(Internship,pk=pk)
            
            serializer=InternshipCompanySerializer(internship)
            return Response(serializer.data,status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    
    def put(self,request,pk):
        try:
            internship=get_object_or_404(Internship,pk=pk)
            if not request.user.is_company or internship.company.user!=request.user:
                return Response({'error': 'You are not authorized to perform this action.'}, status=status.HTTP_403_FORBIDDEN)
            serializer=InternshipCompanySerializer(internship,request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,status=status.HTTP_200_OK)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def delete(self,request,pk):
        try:
            internship=get_object_or_404(Internship,pk=pk)

            if not request.user.is_company or internship.company.user!=request.user:
                return Response({'error': 'You are not authorized to perform this action.'}, status=status.HTTP_403_FORBIDDEN)
            internship.delete()
            return Response({'message':'data deleted'},status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({'error':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ApplicationListView(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        try:
            if request.user.is_company:
                applications=Application.objects.filter(internship__company__user=request.user)
            elif request.user.is_student:
                applications=Application.objects.filter(student__user=request.user)
            else:
                return Response({'error': 'Unauthorized user type.'}, status=status.HTTP_403_FORBIDDEN)
            paginator = PageNumberPagination()
            paginator.page_size = 3  
            result_page = paginator.paginate_queryset(applications, request)
            serializer=ApplicationSerializer(result_page,many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class ApplicationCreateView(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request):
        try:
            if not request.user.is_student:
                return Response({'error': 'You are not authorized to create application.'}, status=status.HTTP_403_FORBIDDEN)
            serializer=ApplicationSerializer(data=request.data,context={'request':request})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,status=status.HTTP_201_CREATED)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
# class ApplicationStatusUpdateView(APIView):
#     permission_classes=[IsAuthenticated]
#     def patch(self,request,pk):
#         try:
#             application=Application.objects.select_related('internship__company').get(pk=pk)
#             if request.user != application.internship.company.user:
#                 return Response({'error': 'You do not have permission to update this application.'},
#                                 status=status.HTTP_403_FORBIDDEN)
#             serializer=ApplicationStatusUpdateSerializer(application,request.data,partial=True)
#             if serializer.is_valid():
#                 serializer.save()
#                 student_email = application.student.user.email
#                 student_name = application.student.user.username
#                 internship_title = application.internship.title
#                 new_status = serializer.validated_data.get('status', application.status)

#                 send_mail(
#                     subject='Your Application Status Has Been Updated',
#                     message=(
#                         f"Hello {student_name},\n\n"
#                         f"Your application for the internship '{internship_title}' has been updated to: {new_status}.\n\n"
#                         "Thank you for using our platform.\n"
#                         "— Internship Management Team"
#                     ),
#                     from_email=settings.DEFAULT_FROM_EMAIL,
#                     recipient_list=[student_email],
#                     fail_silently=False,
#                 )

#                 return Response(serializer.data, status=status.HTTP_200_OK)
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#         except Application.DoesNotExist:
#             return Response({'error': 'Application not found.'}, status=status.HTTP_404_NOT_FOUND)
#         except Exception as e:
#             return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
class ApplicationDetailView(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        try:
            if request.user.is_student:
                application=Application.objects.filter(student=request.user.student_profile)
            elif request.user.is_company:
                application=Application.objects.filter(internship__company=request.user.company_profile)
            else:
                return Response({'error': 'Unauthorized user type.'}, status=status.HTTP_403_FORBIDDEN)

            serializer=ApplicationSerializer(application,many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    
    def put(self,request,pk):
        try:
            application=get_object_or_404(Application,pk=pk)
            serializer=ApplicationSerializer(application,request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,status=status.HTTP_200_OK)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def delete(self,request,pk):
        try:
            application=get_object_or_404(Application,pk=pk)
            application.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({'error':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
@login_required
def view_application(request,pk):
    application = get_object_or_404(Application, pk=pk)
    student_user = application.student
    student_profile = student_user.user
    context={'application': application,
        'student_user': student_user,
        'student_profile': student_profile,}
    return render(request, 'view_application.html', {'context':context})

@login_required
def download_resume(request, pk):
    application = get_object_or_404(Application, pk=pk)
    resume_file = application.student.resume 
    if not resume_file:
        raise Http404("Resume not found.")

    file_path = resume_file.path
    return FileResponse(open(file_path, 'r'), content_type='application/pdf')


def update_application_status(request, pk, action):
    app = get_object_or_404(Application, pk=pk)

    if action == 'accept':
        app.status = 2
        status_text = 'Accepted'
    elif action == 'reject':
        app.status = 3
        status_text = 'Rejected'
    else:
        status_text = 'Updated'

    app.save()

    # Assuming Application model has a ForeignKey to Student/User
    student_email = app.student.user.email  

    # Send email
    send_mail(
        subject='Your Internship Application Status Has Been Updated',
        message=f'Dear {app.student.user.username},\n\nYour application for "{app.internship.title}" has been {status_text}.\n\nThank you.',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[student_email],
        fail_silently=False,
    )

    return redirect('company_dashboard')







        
        
    
        
    
                


        



    




    
