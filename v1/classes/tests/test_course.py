from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from accounts.models import User
from classes.models import Course
import pytest, json


@pytest.mark.django_db
class TestCourse:

    def setup(self):
        '''Create 2 users and a course'''
        
        self.user = User.objects.create_user(email="user1@test.com",
             password="1234TestUser")

        self.superuser = User.objects.create_superuser(email="superuser@test.com",
             password="1234TestUser")


        self.course = Course.objects.create(title="title", teacher=self.superuser, price="12", published=True)

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
