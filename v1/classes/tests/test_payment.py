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
     

     def test_payment_list(self):
          '''
               Anon user gets 403 cuz this api is login required.
               Normal users can only see their transactions (in this test user has 1 transaction)
               Admin users can see all transactions.
          '''

          # request as anon user
          request = self.client.get(reverse("v1_classes:payment-list"))
          assert request.status_code == status.HTTP_403_FORBIDDEN

          # login as a normal user and see only 1 record
          self.client.login(email='user1@test.com', password='1234TestUser')
          request = self.client.get(reverse("v1_classes:payment-list"))
          assert request.status_code == status.HTTP_200_OK

          assert json.loads((request.content))["count"] != 0
          assert json.loads((request.content))["count"] == 1

          self.client.logout()
          self.client.login(email='superuser@test.com', password='1234TestUser')
          
          # superuser can see simple users records/
          request = self.client.get(reverse("v1_classes:payment-list"))
          assert request.status_code == status.HTTP_200_OK

          assert json.loads((request.content))["count"] != 0
          assert json.loads((request.content))["count"] == 1


     def test_payment_detail(self):
          '''
               Anon users can not access payment detail page.
               Admins can see all detail pages.
               Normal users can see their own payment detail pages.
          '''
          
          request = self.client.get(reverse("v1_classes:payment-detail", kwargs={"token" : self.payment.token}))
          assert request.status_code == status.HTTP_403_FORBIDDEN

          self.client.login(email='superuser@test.com', password='1234TestUser')
          request = self.client.get(reverse("v1_classes:payment-detail", kwargs={"token" : self.payment.token}))
          assert request.status_code == status.HTTP_200_OK

          self.client.logout()
          self.client.login(email='user1@test.com', password='1234TestUser')

          request = self.client.get(reverse("v1_classes:payment-detail", kwargs={"token" : self.payment.token}))
          assert request.status_code == status.HTTP_200_OK

     def test_purchase_course(self):
          '''
               Anon users can not purchase items.
               Course provider can not purchase his own item.
               Users that have purchased an item can not do that again.
          '''
          # anon user gets 403
          request = self.client.post(reverse("v1_classes:course-purchase-course", kwargs={"token" : self.course.token}))
          assert request.status_code == status.HTTP_403_FORBIDDEN
          
          # get 400 cuz superuser is the course provider
          self.client.login(email='superuser@test.com', password='1234TestUser')
          request = self.client.post(reverse("v1_classes:course-purchase-course", kwargs={"token" : self.course.token}))
          assert request.status_code == status.HTTP_400_BAD_REQUEST

          self.client.logout()
          self.client.login(email='user1@test.com', password='1234TestUser')
          # get 400 cuz item is already purchased
          request = self.client.post(reverse("v1_classes:course-purchase-course", kwargs={"token" : self.course.token}))
          assert request.status_code == status.HTTP_400_BAD_REQUEST

          User.objects.create_user(email="user2@test.com",password="1234TestUser", balance=200)

          self.client.logout()
          self.client.login(email='user2@test.com', password='1234TestUser')
          # get success
          request = self.client.post(reverse("v1_classes:course-purchase-course", kwargs={"token" : self.course.token}))
          assert request.status_code == status.HTTP_200_OK