from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.response import Response
from rest_framework import status
from api.v1.user.serializers import UserSerializer, CourseSerializer
from django.db import IntegrityError
from django.contrib.auth import get_user_model
from app.models import Courses
import pytz
from datetime import datetime

User = get_user_model()


class UserList(ListAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserProfile(RetrieveAPIView):
    permission_classes = [IsAdminUser]
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
    permission_classes = [IsAdminUser]
    serializer_class = CourseSerializer

    def post(self, request, *args, **kwargs):
        course_name = request.data.get('course_name')
        user_id = request.data.get('user')
        user = User.objects.get(id=user_id)
        assigned_on = datetime.now()
        expires_on = datetime.strptime(request.data.get('expires_on'), '%Y-%m-%dT%H:%M:%S.%fZ')
        expires_on = expires_on.replace(tzinfo=pytz.UTC)
        
        course = Courses.objects.create(
            name=course_name,
            user=user,
            assigned_on=assigned_on,
            expiry_date=expires_on
        )

        serializer = self.serializer_class(course)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CompletedCourses(ListAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = CourseSerializer

    def get_queryset(self):
        user_id = self.kwargs['pk']
        queryset = Courses.objects.filter(user_id=user_id, is_completed=True)
        return queryset


class PendingCourses(ListAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = CourseSerializer

    def get_queryset(self):
        user_id = self.kwargs['pk']
        queryset = Courses.objects.filter(user=user_id, is_completed=False)
        return queryset


class AddUser(CreateAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        # Create a new Member object with the given data
        name = request.data.get('name', None)
        email = request.data.get('email', None)
        phone = request.data.get('phone', None)
        _domain = request.data.get('domain', None)
        domain = 'dev' if _domain == 'dev' else 'sec'
        password = email # set password to email
        is_admin = request.data.get('is_admin', False)
        user = User.objects.create_user(name=name, email=email, phone_number=phone, domain=domain, password=password, is_superuser=is_admin, is_staff=is_admin)
        user.save()
        serializer = self.get_serializer(user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
