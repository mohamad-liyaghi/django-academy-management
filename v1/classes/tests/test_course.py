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

