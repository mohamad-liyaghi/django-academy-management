from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from accounts.models import User
from classes.models import Course, Payment
import pytest, json


@pytest.mark.django_db
class TestPayment:
    def setup(self):
        '''Create 2 users, one course and one payment.'''
        
        self.user = User.objects.create_user(email="user1@test.com",
             password="1234TestUser", balance=200)

        self.superuser = User.objects.create_superuser(email="superuser@test.com",
             password="1234TestUser")


        self.course = Course.objects.create(title="title", teacher=self.superuser, price="12", published=True)
        self.payment = Payment.objects.create(user=self.user, course=self.course)

        self.client = APIClient()
