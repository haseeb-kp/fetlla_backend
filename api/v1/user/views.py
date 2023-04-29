# class CompletedCourses(ListAPIView):
#     serializer_class = CourseSerializer

#     def get_queryset(self):
#         user = self.request.user
#         queryset = Courses.objects.filter(user=user, is_completed=True)
#         return queryset

# class PendingCourses(generics.ListAPIView):
#     serializer_class = CourseSerializer

#     def get_queryset(self):
#         user = self.request.user
#         queryset = Course.objects.filter(user=user, is_completed=False)
#         return queryset