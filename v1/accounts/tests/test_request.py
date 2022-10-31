from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from accounts.models import User, Request
import pytest, json


@pytest.mark.django_db
class TestRequest:

    def setup(self):
        '''Create a simple user and a superuser'''
        self.superuser = User.objects.create_superuser(email="superuser@test.com",
             password="1234TestSuperuser")

        self.user = User.objects.create_user(email="user@test.com",
             password="1234TestUser")

        self.client = APIClient()


    def test_profile_list(self):
        '''
            Test for creating requests.
            Anon users can not create requests.
            Superusers can not create request to become admin or teacher cuz permissions were given.
            '''

        url = reverse("v1:request-list")

        # send request as an anon user
        request = self.client.post(url, data={"role" : "a"}, format="json")
        assert request.status_code == status.HTTP_403_FORBIDDEN

        # login as superuser
        self.client.login(email='superuser@test.com', password='1234TestSuperuser')

        # superuser cant create request cuz permissions were given.
        request = self.client.post(url, data={"role" : "a"}, format="json")
        assert request.status_code == status.HTTP_400_BAD_REQUEST

        # logout and login as user
        self.client.logout()
        self.client.login(email='user@test.com', password='1234TestUser')

        # check is there any request
        assert self.user.requests.count() == 0
        # create request
        request = self.client.post(url, data={"role" : "a"}, format="json")
        assert request.status_code == status.HTTP_201_CREATED
        assert self.user.requests.count() == 1

        # user cant create another request cuz he has a pending request
        request = self.client.post(url, data={"role" : "a"}, format="json")
        assert request.status_code == status.HTTP_400_BAD_REQUEST


        