import logging
from rest_framework import status
from .models import Student
from .serializers import StudentSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from email_pro.utils import send_email


error_logger = logging.getLogger('error_logger')
success_logger = logging.getLogger('success_logger')

class StudentAPI(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        try:
            students = Student.objects.all()
            serializer = StudentSerializer(students , many=True)
            success_logger.info("Students fetched successfully")
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            error_logger.error("There is an error")
            return Response(data={'detail': "There is an error feching the students"}, status=status.HTTP_400_BAD_REQUEST)
        

    def post(self, request):
        try:
            serializer = StudentSerializer(data=request.data, context={'request': request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            
            success_logger.info(f"Student with id {serializer.data.get('id')} created successfully")
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            error_logger.error(f"Failed to create student : {serializer.errors}")
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class StudentDetailsAPI(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        try:
            students =get_object_or_404(Student, pk=pk)
            serializer = StudentSerializer(students)
            success_logger.info(f"students deatils fetched : {serializer.data}")
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            error_logger.error(f"There is an error fetching the students")
            return Response(data= serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def patch(self, request, pk=None):
        try:
            students = get_object_or_404(Student, pk=pk)
            serializer = StudentSerializer(students, data=request.data)
            if serializer.is_valid():
                instance = serializer.save()
                success_logger.info(f"Student updated: {instance}")
                return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            error_logger.error(f"failed to update student {pk}: {serializer.errors}")
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        try:
            students =get_object_or_404(Student, pk=pk)
            students.save()
            success_logger.info(f"student delete successfully: {pk}")
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            error_logger.error(f"failed to delete student")
            return Response(data= {'detail': 'Error deleting studets'}, status=status.HTTP_400_BAD_REQUEST)        


