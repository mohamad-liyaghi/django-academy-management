from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from accounts.models import User
from classes.models import Course, Payment
import pytest, json


@pytest.mark.django_db
class TestPayment:
    pass