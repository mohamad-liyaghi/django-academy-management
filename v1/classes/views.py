from rest_framework.viewsets import ModelViewSet
from django.shortcuts import get_object_or_404
from rest_framework import filters
from django.http import Http404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status


from classes.models import Course, Payment
from classes.serializers import (AddCourseSerializer, CourseListSerializer, CourseDetailSerializer, 
                                    CoursePublishSerializer, PaymentListSerializer, PaymentDetailSerializer,
                                     PurchaseCourseSerializer, SessionListSerializer, SessionCreateSerializer)
from .permissions import CoursePermission
from .viewsets import ListRetrieveViewSet


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
        print(self.action)
        if self.action == "create":
            return AddCourseSerializer

        elif self.action == 'list':
            return CourseListSerializer
        
        elif self.action in ["retrieve", "update", "partial_update"]:
            return CourseDetailSerializer
        
        elif self.action == "publish_course":
            return CoursePublishSerializer
        
        elif self.action == "purchase_course":
            return PurchaseCourseSerializer
        
        elif self.action == 'session' and self.request.method == "GET":
            return SessionListSerializer
        
        elif self.action == 'session' and self.request.method == "POST":
            return SessionCreateSerializer


    def update(self, request, *args, **kwargs):
        '''only teacher can update the course'''

        if self.get_object().teacher == self.request.user:
            return super().update(request, *args, **kwargs)

        else:
            return Response("You are not allowed to update this object", status=status.HTTP_403_FORBIDDEN)

    
    @action(detail=True, methods=["GET", "POST"], url_path="publish")
    def publish_course(self, request, token):
        object = get_object_or_404(Course, token=token, teacher=request.user)

        if request.method == "GET":
            if object.published:
                return Response("Course is published. post to unpublish.", status=status.HTTP_200_OK)

            return Response("Course is unpublished. post to publish.", status=status.HTTP_200_OK)
            
            
        elif request.method == "POST":

            if object.published:
                if object.students.count() > 0:
                    return Response("Course is in use by students.", status=status.HTTP_400_BAD_REQUEST)
                    
                object.published = False
                object.save()
                return Response("Course unpublished!.", status=status.HTTP_200_OK)


            else:
                object.published = True
                object.save()
                return Response("Course published!.", status=status.HTTP_200_OK)


    @action(detail=True, methods=["GET", "POST"], url_path="pay", permission_classes=[IsAuthenticated,])
    def purchase_course(self, request, token):
        object = get_object_or_404(Course, token=token, published=True)

        if request.method == "GET":
            return Response(f"Course price is {object.price}, if  you want to purchase, post this url.", 
                                status=status.HTTP_200_OK)
        
        elif request.method == "POST":
            if object.teacher == request.user:
                return Response("You cant buy your own course.",
                                     status=status.HTTP_400_BAD_REQUEST)

            if object.students.filter(user=self.request.user, course=object):
                return Response("You have already purchased this item.",
                                     status=status.HTTP_400_BAD_REQUEST)

            if int(request.user.balance) < int(object.price):
                return Response("You dont have enough money to purchase this course.",
                                     status=status.HTTP_400_BAD_REQUEST)

            Payment.objects.create(user=self.request.user, course=object)
            # costing stuff will be executed after we create payment record.
            return Response("You have successfully purchased this course.", 
                            status=status.HTTP_200_OK)

    @action(detail=True, methods=["GET", "POST"], url_path="sessions", permission_classes=[IsAuthenticated,], )
    def session(self, request, token):
        object = self.get_object()

        if request.method == "GET":

            if object.students.filter(user=self.request.user, course=object) \
                or object.teacher == request.user :
                serializer = SessionListSerializer(object.sessions.all(), many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)

            return Response("You have to purchase this item.", status=status.HTTP_403_FORBIDDEN)

        elif request.method == "POST":
            
            # only admin can add link
            if request.user == object.teacher:
                data = SessionCreateSerializer(data=request.POST)
                video = request.data['video']
                attachment = request.data['attachment']

                if data.is_valid():
                    data.save(course=object, video=video, attachment=attachment)
                    return Response(data.data, status=status.HTTP_201_CREATED)
                
                return Response(data.errors, status=status.HTTP_400_BAD_REQUEST)

            return Response("only teachers can add sessions.", status=status.HTTP_403_FORBIDDEN)

        
            
                       
 
class PaymentViewSet(ListRetrieveViewSet):
    '''A viewset to purchase a course and see transaction `list` and `detail`.'''

    permission_classes = [IsAuthenticated,]
    lookup_field = "token"

    def get_serializer_class(self):
        if self.action == "list":
            return PaymentListSerializer

        elif self.action == "retrieve":
            return PaymentDetailSerializer
    

    def get_queryset(self):
        '''Admins can see new transactions but normal users can onlu see their transactions.'''
        
        if self.request.user.role in ["su", "ad"]:
            return Payment.objects.all().order_by("-date")

        return Payment.objects.filter(user=self.request.user).order_by("-date")
    

    def get_object(self):
        if self.request.user.role in ["su", "ad"]:
            return super().get_object()
        
        return get_object_or_404(Payment, token=self.kwargs["token"], 
                                user=self.request.user)