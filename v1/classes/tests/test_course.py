from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from accounts.models import User
from classes.models import Course, Session
import pytest, json


@pytest.mark.django_db
class TestCourse:

    def setup(self):
        '''Create 2 users and a course'''
        
        self.user = User.objects.create_user(email="user1@test.com",
             password="1234TestUser", balance=200)

        self.superuser = User.objects.create_superuser(email="superuser@test.com",
             password="1234TestUser")


        self.course = Course.objects.create(title="title", teacher=self.superuser, price="12", published=True)
        self.session = Session.objects.create(course=self.course, title="Test session")

        self.client = APIClient()



    def test_get_course_list(self):
        '''Everyone can visit this page and see all published courses.'''

        request = self.client.get(reverse("v1_classes:course-list"))

        assert json.loads((request.content))["count"] == 1
        assert json.loads((request.content))["count"] != 2
        assert request.status_code == status.HTTP_200_OK


    def test_add_course(self):
        '''Anon/Normal users can not add courses but teachers/superuser/admins can.'''

        # anon users can not add course
        request = self.client.post(reverse("v1_classes:course-list"), data={"title" : "title"})
        assert request.status_code == status.HTTP_403_FORBIDDEN

        # login as normal user
        self.client.login(email='user@test.com', password='1234TestUser')

        # request and get 403 cuz user is not allowed
        request = self.client.post(reverse("v1_classes:course-list"), data={"title" : "title"})
        assert request.status_code == status.HTTP_403_FORBIDDEN

        # logout and login as superuser
        self.client.logout()
        self.client.login(email='superuser@test.com', password='1234TestUser')

        assert self.superuser.courses.count() == 1

        # request and check if its created
        request = self.client.post(reverse("v1_classes:course-list"), data={"title" : "title", "description" : "description"})

        assert request.status_code == status.HTTP_201_CREATED
        assert self.superuser.courses.count() == 2

    
    def test_get_course_detail(self):
        '''
            Users can see published course details.
            But course owner can see the course if it is un published.
        '''

        # create an unpublished course
        course_2 = Course.objects.create(title="title", teacher=self.superuser, price="12")

        # anon user gets 404 cuz course is not published
        request = self.client.get(reverse("v1_classes:course-detail", kwargs={"token" : course_2.token}))
        assert request.status_code == status.HTTP_404_NOT_FOUND

        # anon user can see published course detail page
        request = self.client.get(reverse("v1_classes:course-detail", kwargs={"token" : self.course.token}))
        assert request.status_code == status.HTTP_200_OK

        self.client.login(email='superuser@test.com', password='1234TestUser')
        # superuser can see the page cuz its his own course
        request = self.client.get(reverse("v1_classes:course-detail", kwargs={"token" : course_2.token}))
        assert request.status_code == status.HTTP_200_OK

        self.client.logout()
        self.client.login(email='user@test.com', password='1234TestUser')
        
        # normal user can see superusers unpub course
        request = self.client.get(reverse("v1_classes:course-detail", kwargs={"token" : course_2.token}))
        assert request.status_code == status.HTTP_404_NOT_FOUND

        # normal user can see published course page
        request = self.client.get(reverse("v1_classes:course-detail", kwargs={"token" : self.course.token}))
        assert request.status_code == status.HTTP_200_OK


    def test_update_course(self):
        '''
            Anon users can not update courses.
            Only course teachers can update their own courses.
        '''
        
        # anon user gets 403
        request = self.client.patch(reverse("v1_classes:course-detail", kwargs={"token" : self.course.token}), 
                data={"title" : "new title"})
        assert request.status_code == status.HTTP_403_FORBIDDEN

        # normal user gets 403
        self.client.login(email='user@test.com', password='1234TestUser')
        request = self.client.patch(reverse("v1_classes:course-detail", kwargs={"token" : self.course.token}), 
                data={"title" : "new title"})

        assert request.status_code == status.HTTP_403_FORBIDDEN

        self.client.logout()
        self.client.login(email='superuser@test.com', password='1234TestUser')

        # course owner gets 200
        request = self.client.patch(reverse("v1_classes:course-detail", kwargs={"token" : self.course.token}), 
                data={"title" : "new title"}, format="json")

        assert request.status_code == status.HTTP_200_OK

    
    def test_publish_course(self):
        '''
            Only course owner can publish and un publish the course
        '''
        # create a couse
        course = Course.objects.create(title="title", teacher=self.superuser, price="12")

        # request as anon user and get 403
        request = self.client.post(reverse("v1_classes:course-publish-course", kwargs={"token" : course.token}))
        assert request.status_code == status.HTTP_403_FORBIDDEN
        
        # request as normal user and get 403 cuz permission denied
        self.client.login(email='user@test.com', password='1234TestUser')
        request = self.client.post(reverse("v1_classes:course-publish-course", kwargs={"token" : course.token}))
        assert request.status_code == status.HTTP_403_FORBIDDEN
        
        self.client.logout()
        self.client.login(email='superuser@test.com', password='1234TestUser')
        # request as superuser and get 200 cuz user is courses teacher
        request = self.client.post(reverse("v1_classes:course-publish-course", kwargs={"token" : course.token}))
        assert request.status_code == status.HTTP_200_OK

    
    def test_get_course_sessions(self):
        '''
            Anon users get 403.
            Users who hasnt purchased the course get 403.
            Course owner and teacher gets 200.
        '''
        request = self.client.get(reverse("v1_classes:course-session", kwargs={"token" : self.course.token}))
        assert request.status_code == status.HTTP_403_FORBIDDEN

        self.client.login(email='user@test.com', password='1234TestUser')
        request = self.client.get(reverse("v1_classes:course-session", kwargs={"token" : self.course.token}))
        assert request.status_code == status.HTTP_403_FORBIDDEN

        self.client.logout()
        self.client.login(email='superuser@test.com', password='1234TestUser') 
        request = self.client.get(reverse("v1_classes:course-session", kwargs={"token" : self.course.token}))
        assert request.status_code == status.HTTP_200_OK
    

    def test_add_session(self):
        '''
            Anon users can not add sessions.
            Normal users can not add sessions.
            Teachers can add sessions to their own courses.
        '''
        # anon user gets 403
        request = self.client.post(reverse("v1_classes:course-session",
                                             kwargs={"token" : self.course.token}), data={"title" : "test"})

        assert request.status_code == status.HTTP_403_FORBIDDEN

        # normal users get 403
        self.client.login(email='user@test.com', password='1234TestUser')
        request = self.client.post(reverse("v1_classes:course-session",
                                             kwargs={"token" : self.course.token}), data={"title" : "test"})

        assert request.status_code == status.HTTP_403_FORBIDDEN

        self.client.logout()
        self.client.login(email='superuser@test.com', password='1234TestUser') 
        # if data is invalid we will get 400 bad request
        request = self.client.post(reverse("v1_classes:course-session",
                                             kwargs={"token" : self.course.token}))

        assert request.status_code == status.HTTP_400_BAD_REQUEST
        
        # if data if ok, session will be created
        request = self.client.post(reverse("v1_classes:course-session",
                                             kwargs={"token" : self.course.token}), data={"title" : "test"})

        assert request.status_code == status.HTTP_201_CREATED

    
    def test_session_detail(self):
        '''
            Anon users can not access this page.
            Users who hasnt purchased, can not access this page.
            Course teacher and people who has purchased this item, can access this page.
        '''
        
        request = self.client.get(reverse("v1_classes:course-session-detail", kwargs={"token" : self.course.token, 
            "session_token" : self.session.token}))

        assert request.status_code == status.HTTP_403_FORBIDDEN

        self.client.login(email='user@test.com', password='1234TestUser')
        request = self.client.get(reverse("v1_classes:course-session-detail", kwargs={"token" : self.course.token, 
            "session_token" : self.session.token}))

        assert request.status_code == status.HTTP_403_FORBIDDEN

        self.client.logout()
        self.client.login(email='superuser@test.com', password='1234TestUser') 
        request = self.client.get(reverse("v1_classes:course-session-detail", kwargs={"token" : self.course.token, 
            "session_token" : self.session.token}))

        assert request.status_code == status.HTTP_200_OK