from rest_framework.viewsets import ModelViewSet
from django.shortcuts import get_object_or_404
from rest_framework import filters

from rest_framework.response import Response
from rest_framework.decorators import action

from classes.models import Course
from v1.classes.serializers import AddCourseSerializer, CourseListSerializer
from .permissions import CoursePermission


class CourseViewSet(ModelViewSet):
    '''A viewset for Course stuff such as `add`, `list`, `delete`, and so on'''

    permission_classes = [CoursePermission,]
    search_fields = ['title', "price", "difficulty"]
    filter_backends = (filters.SearchFilter,)


    def get_serializer_context(self):
        return {'user' : self.request.user}


    def get_queryset(self):
        '''If user is authenticated it will return users courses + all courses.
            otherwise it returns course list.'''

        if self.request.user.is_authenticated:
            all_courses = Course.objects.filter(published=True)
            user_courses = Course.objects.filter(teacher=self.request.user)
            # combine 2 queries
            mixed_query = user_courses | all_courses
            return mixed_query.order_by("-id")

        return Course.objects.filter(published=True).order_by("-id")


    def get_serializer_class(self):
        if self.action == "create":
            return AddCourseSerializer

        elif self.action == 'list':
            return CourseListSerializer
