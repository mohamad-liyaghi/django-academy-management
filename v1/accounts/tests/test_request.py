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


    def test_create_request(self):
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

    
    def test_get_request_list(self):
        '''
            Anon users can not access list request page.
            Normal users can just see their own requests.
            Suerusers can see all requests.
        '''
        
        url = reverse("v1:request-list")

        # return forbidden cuz user is not authenticated
        request = self.client.get(url)
        assert request.status_code == status.HTTP_403_FORBIDDEN

        # login as normal user
        self.client.login(email='user@test.com', password='1234TestUser')

        # create request
        request = self.client.post(url, data={"role" : "a"}, format="json")
        assert request.status_code == status.HTTP_201_CREATED

        request = self.client.get(url)
        # number of requests
        assert json.loads((request.content))["count"] == 1
        assert request.status_code == status.HTTP_200_OK


        self.client.logout()

        # login as superuser
        self.client.login(email='superuser@test.com', password='1234TestSuperuser')

        # superuser can see all requests
        request = self.client.get(url)

        # number of requests
        assert json.loads((request.content))["count"] == 1
        assert request.status_code == status.HTTP_200_OK

    
    def test_block_request(self):
        '''Block a user's request. so that user can not request anymore'''
        # login as normal user
        self.client.login(email='user@test.com', password='1234TestUser')

        # create request
        request = self.client.post(reverse("v1:request-list"), data={"role" : "a"}, format="json")
        assert request.status_code == status.HTTP_201_CREATED

        self.client.logout()

        # login as superuser
        self.client.login(email='superuser@test.com', password='1234TestSuperuser')

        # block user's request
        request = self.client.put(reverse("v1:request-detail", kwargs={"pk" : self.user.requests.first().id.hex}),
        data={"status" : "b"})
        assert request.status_code == status.HTTP_200_OK

        # login as normal user
        self.client.logout()
        self.client.login(email='user@test.com', password='1234TestUser')

        # get 400 after request cuz user is blocked
        request = self.client.post(reverse("v1:request-list"), data={"role" : "a"}, format="json")
        assert request.status_code == status.HTTP_400_BAD_REQUEST


    def test_accept_user_request(self):
        '''Accept users requests and update their role'''

        # login as normal user
        self.client.login(email='user@test.com', password='1234TestUser')

        # create request
        request = self.client.post(reverse("v1:request-list"), data={"role" : "a"}, format="json")
        assert request.status_code == status.HTTP_201_CREATED

        self.client.logout()

        # login as superuser
        self.client.login(email='superuser@test.com', password='1234TestSuperuser')

        # accept user's request
        request = self.client.put(reverse("v1:request-detail", kwargs={"pk" : self.user.requests.first().id.hex}),
        data={"status" : "a"})
        assert request.status_code == status.HTTP_200_OK

        # check if request status updated
        assert json.loads(request.content)["status"]  == "a"




