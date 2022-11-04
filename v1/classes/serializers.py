from rest_framework import serializers
from rest_framework.exceptions import APIException
from classes.models import Course


class AddCourseSerializer(serializers.ModelSerializer):
    '''A serializer to add a course'''

    token = serializers.CharField(read_only=True)
    published = serializers.BooleanField(read_only=True)
    teacher = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Course
        fields = ["title", 'description', 'teacher', 'price', 'difficulty', 'time', 'token', "published"]
    

    def save(self, **kwargs):
        '''Check if user is admin/teacher to add a course'''

        user = self.context["user"]

        if user.role in ["su", 'ad', 't']:
            return super().save(teacher=self.context["user"], **kwargs)

        raise APIException("User is not allowed to add course")
        