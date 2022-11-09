from rest_framework import serializers
from rest_framework.exceptions import APIException
from classes.models import Course, Payment


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



class CourseListSerializer(serializers.ModelSerializer):

    teacher = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Course
        fields = ["title", "teacher", "price", "difficulty", "token"]
        


class CourseDetailSerializer(serializers.ModelSerializer):

    lookup_field = "token"
    teacher = serializers.StringRelatedField()
    token = serializers.CharField(read_only=True)
    published = serializers.BooleanField(read_only=True)
    # TODO: add a field in order to see if this course is purchased or not

    class Meta:
        model = Course
        fields = ["title", "teacher", "price", "difficulty",
                        "time", "description", "published", "token"]


class CoursePublishSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course 
        fields = []


class PaymentListSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Payment
        fields = ["token", "amount", "date"]


class PaymentDetailSerializer(serializers.ModelSerializer):

    course = serializers.StringRelatedField()
    user = serializers.StringRelatedField()

    class Meta:
        model = Payment
        fields = ["token", "course", "user", "amount", "date"]