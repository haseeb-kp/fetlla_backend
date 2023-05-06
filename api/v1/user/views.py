from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.response import Response
from rest_framework import status
from api.v1.user.serializers import UserSerializer, CourseSerializer
from django.db import IntegrityError
from django.contrib.auth import get_user_model
from app.models import Courses

User = get_user_model()

class CompletedCourses(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CourseSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = Courses.objects.filter(user=user, is_completed=True)
        return queryset

class PendingCourses(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CourseSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = Courses.objects.filter(user=user, is_completed=False)
        return queryset

class MarkAsCompleted(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CourseSerializer
    queryset = Courses.objects.all()

    def update(self, request, *args, **kwargs):
        course_id = kwargs['pk']
        print("course_id = ",course_id)
        instance = Courses.objects.filter(id=course_id, user=request.user).first()
        instance.mark_as_completed()
        return Response(status = status.HTTP_200_OK)