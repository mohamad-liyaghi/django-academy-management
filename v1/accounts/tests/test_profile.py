from accounts.models import User, Profile
import pytest


@pytest.mark.django_db
class TestProfile:
    
    def setup(self):
        '''Create a simple user and a superuser'''
        self.superuser = User.objects.create_superuser(email="superuser@test.com",
             password="1234TestSuperuser")

        self.user = User.objects.create_user(email="user@test.com",
             password="1234TestUser")


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