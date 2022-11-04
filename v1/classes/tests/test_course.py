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


        self.course = Course.objects.create(title="title", teacher=self.superuser, price="12")

        self.client = APIClient()
