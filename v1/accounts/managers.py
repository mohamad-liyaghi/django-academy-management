from django.contrib.auth.models import BaseUserManager
import random
from django.db.models import manager


class UserManager(BaseUserManager):
    '''Custom user manager'''

    def create_user(self, email, password, **kwargs):

        if not email:
            raise ValueError("Users must have Email")


        token = random.randint(1, 99999999999999)
        email = self.normalize_email(email)

        user = self.model(
            email=email, token=token, **kwargs
        )

        user.set_password(password)
        user.save(using= self._db)

        return user


    def create_superuser(self, email, password, **kwargs):
        '''Create a superuser'''

        user = self.create_user(email=email,  password=password,
            role="su", is_staff=True, is_superuser=True, is_active=True)
        user.save(using=self._db)
        return user


class RequestManager(manager.Manager):
    def create(self, **kwargs):
        user = kwargs["user"]

        if user.role in ["su", "ad"]:
            raise ValueError('Given user is admin and rights were given.')

        if user.role == "t" and kwargs["role"] == "t":
            raise ValueError("Given user is already a teacher")

        if user.requests.filter(status="p").exists():
            raise ValueError("You have already a pending request.")


        def check_kw_exist(name):
            '''Check if kw is passed'''
            try:
                return kwargs[name]
            except:
                return None


        request = self.model(user=user, role=kwargs["role"],
            attachment=check_kw_exist("attachment"),
            description=check_kw_exist("description"))

        request.save()

        return request
        
