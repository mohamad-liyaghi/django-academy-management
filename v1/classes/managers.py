import random
from django.db.models import manager


class CourseManager(manager.Manager):
    '''override create method'''

    def create(self, **kwargs):
        teacher = kwargs["teacher"]

        if not teacher.role in ["ad", "su", "t"]:
            raise ValueError("User is not allowed to add course.")
        
        try:
            kwargs["description"]
        except:
            kwargs.setdefault('description', "No description available.")

        course = self.model(token=random.randint(1, 999999999999999), **kwargs)
        course.save()

        return course

        