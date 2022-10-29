from rest_framework.test import APIClient
from rest_framework import status
from accounts.models import User, Profile
import pytest, json


@pytest.mark.django_db
class TestProfile:

    def setup(self):
        '''Create a simple user and a superuser'''
        self.superuser = User.objects.create_superuser(email="superuser@test.com",
             password="1234TestSuperuser")

        self.user = User.objects.create_user(email="user@test.com",
             password="1234TestUser")

        self.client = APIClient()


    def test_check_profiles_are_created(self):
        '''Test signals to see if they create profile after registering users.'''

        assert Profile.objects.filter(user=self.superuser).exists() == True
        assert Profile.objects.filter(user=self.user).exists() == True


    def test_check_users_role(self):

        assert self.superuser.is_superuser == True
        assert self.superuser.role == "su"

        assert self.user.is_superuser == False
        assert self.user.role == 's'


    def test_check_tokens_are_different(self):
        assert self.user.token != self.superuser.token

    
    def test_profile_list_page(self):
        '''We expect superusers to see users list
            but simple users can just watch their profile token'''

        # unregistered user get 403 cuz this page is login required
        response = self.client.get("/v1/accounts/")
        assert response.status_code == status.HTTP_403_FORBIDDEN

        # login as superuser and send request
        self.client.login(email='superuser@test.com', password='1234TestSuperuser')
        response = self.client.get("/v1/accounts/")
        # check if there are 2 users listed (its list of users).
        assert json.loads((response.content))["count"] == 2
        assert json.loads((response.content))["count"] != 1

        # logout
        self.client.logout()

        # login as a normal user and send request
        self.client.login(email='user@test.com', password='1234TestUser')
        response = self.client.get("/v1/accounts/")

        # check if only the user is listed
        assert json.loads((response.content))["count"] == 1
        assert json.loads((response.content))["count"] != 2


    def test_get_profile_detail_page(self):
        '''
            Anon users can't view profile pages, 
            Admin users can view everyones profile page,
            Normal users can just access their own profile pages othervise they get 404.(they dont get 403 for query stuff in views)
        '''

        # get superuser and simple user's profile id for url stuff
        user_profile_id = self.user.profile.first().id
        superuser_profile_id = self.superuser.profile.first().id
        
        # anon users get 403 cuz they have to be authenticated
        response = self.client.get(f"/v1/accounts/{user_profile_id}", follow=True)
        assert response.status_code == status.HTTP_403_FORBIDDEN
        

        # login as normal user
        self.client.login(email='user@test.com', password='1234TestUser')

        # get 200 status from users own profile page
        response = self.client.get(f"/v1/accounts/{user_profile_id}", follow=True)
        assert response.status_code == status.HTTP_200_OK

        # get 404 from superusers profile page
        response = self.client.get(f"/v1/accounts/{superuser_profile_id}/", follow=True)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        # log out and login as a superuser
        self.client.logout()
        self.client.login(email='superuser@test.com', password='1234TestSuperuser')

        # get 200 response code when checking users profile page
        response = self.client.get(f"/v1/accounts/{user_profile_id}", follow=True)
        assert response.status_code == status.HTTP_200_OK