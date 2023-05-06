from django.urls import re_path
from . import views


urlpatterns = [
    re_path(r'^user_list/$',views.UserList.as_view()),
    re_path(r'^user_profile/(?P<pk>\d+)/$', views.UserProfile.as_view()),
    re_path(r'^add_course/$',views.AddCourse.as_view()),
    re_path(r'^add_user/$',views.AddUser.as_view()),
    re_path(r'^completed_courses/(?P<pk>\d+)/$', views.CompletedCourses.as_view()),
    re_path(r'^pending_courses/(?P<pk>\d+)/$', views.PendingCourses.as_view()),

    ]