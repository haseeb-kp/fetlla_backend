from django.urls import re_path
from . import views


urlpatterns = [
    re_path(r'^completed_courses/$', views.CompletedCourses.as_view()),
    re_path(r'^pending_courses/$', views.PendingCourses.as_view()),
    re_path(r'^mark_as_completed/(?P<pk>\d+)/$', views.MarkAsCompleted.as_view()),


    ]