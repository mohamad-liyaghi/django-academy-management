from rest_framework import serializers
from rest_framework.exceptions import APIException
from classes.models import Course, Payment, Session


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

    purchases = serializers.SerializerMethodField(method_name='calculate_purchases', read_only=True )
    is_purchased = serializers.SerializerMethodField(method_name="check_item_purchased", read_only=True)

    def calculate_purchases(self, course:Course):
        '''Calculate all purchases'''
        return Payment.objects.filter(course=course).count()
    
    
    def check_item_purchased(self, course:Course):
        '''Check if user purchased the item or not'''
        user = self.context["user"]
        
        if user.is_authenticated:
            return Payment.objects.filter(user=user, course=course).exists()

        return False
    

    class Meta:
        model = Course
        fields = ["title", "teacher", "price", "difficulty",
                        "time", "description", "published", "token", "purchases", "is_purchased"]


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
    

class PurchaseCourseSerializer(CoursePublishSerializer):
    pass


class SessionListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Session
        fields = ["number", "title", "token", "time"]
