from rest_framework.viewsets import ModelViewSet
from django.shortcuts import get_object_or_404
from rest_framework import filters
from django.http import Http404
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status


from classes.models import Course
from v1.classes.serializers import AddCourseSerializer, CourseListSerializer, CourseDetailSerializer
from .permissions import CoursePermission


class CourseViewSet(ModelViewSet):
    '''A viewset for Course stuff such as `add`, `list`, `delete`, and so on'''

    permission_classes = [CoursePermission,]
    search_fields = ['title', "price", "difficulty"]
    filter_backends = (filters.SearchFilter,)
    lookup_field = "token"


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


    def get_object(self):
        query  = get_object_or_404(Course, token=self.kwargs["token"])

        if not query.published:

            if query.teacher == self.request.user:
                return query
            raise Http404

        return query


    def get_serializer_class(self):
        if self.action == "create":
            return AddCourseSerializer

        elif self.action == 'list':
            return CourseListSerializer
        
        elif self.action in ["retrieve", "update", "partial_update"]:
            return CourseDetailSerializer


    def update(self, request, *args, **kwargs):
        '''only teacher can update the course'''

        if self.get_object().teacher == self.request.user:
            return super().update(request, *args, **kwargs)

        else:
            return Response("You are not allowed to update this object", status=status.HTTP_403_FORBIDDEN)
