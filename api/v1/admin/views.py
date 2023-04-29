from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.response import Response
from rest_framework import status
from api.v1.user.serializers import UserSerializer, CourseSerializer
from django.db import IntegrityError
from django.contrib.auth import get_user_model
from app.models import Courses
from datetime import datetime

User = get_user_model()


class UserList(ListAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = UserSerializer

    def get_queryset(self):
        queryset = User.objects.all().exclude(is_superuser=True)
        return queryset

class UserProfile(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
        except User.DoesNotExist:
            return Response({'detail': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

class AddCourse(CreateAPIView):
    serializer_class = CourseSerializer

    def post(self, request, *args, **kwargs):
        name = request.data.get('name')
        user = request.user
        assigned_on = datetime.strptime(request.data.get('assigned_on'), '%d-%m-%Y')
        expires_on = datetime.strptime(request.data.get('expires_on'), '%d-%m-%Y')

        course = Courses.objects.create(
            name=name,
            user=user,
            assigned_on=assigned_on,
            expiry_date=expires_on
        )

        serializer = self.serializer_class(course)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CompletedCourses(ListAPIView):
    serializer_class = CourseSerializer

    def get_queryset(self):
        user_id = self.kwargs['pk']
        queryset = Courses.objects.filter(user_id=user_id, is_completed=True)
        return queryset


class PendingCourses(ListAPIView):
    serializer_class = CourseSerializer

    def get_queryset(self):
        user_id = self.kwargs['pk']
        queryset = Courses.objects.filter(user=user_id, is_completed=False)
        return queryset
