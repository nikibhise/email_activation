from django.urls import path
from .views import StudentAPI, StudentDetailsAPI

urlpatterns = [
    path('students/', StudentAPI.as_view()),
    path('students/<int:pk>/', StudentDetailsAPI.as_view()),
]