from rest_framework.viewsets import ModelViewSet
from django.shortcuts import get_object_or_404

from rest_framework.response import Response
from rest_framework.decorators import action

from classes.models import Course


class CourseViewSet(ModelViewSet):
    '''A viewset for Course stuff such as `add`, `list`, `delete`, and so on'''

    queryset = Course.objects.all()
