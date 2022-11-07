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



class PaymentManager(manager.Manager):
    '''Override create method for payments'''

    def create(self, **kwargs):

        course = kwargs["course"]
        user = kwargs["user"]

        if not course.published:
            raise ValueError("Course is not published")

        if user in course.students.all():
            raise ValueError("User has already purchased this item.")

        if user == course.teacher:
            raise ValueError("Teachers can not buy their own courses.")

        if user.balance < course.price:
            raise ValueError("User dont have enough money.")

        payment = self.model(token=random.randint(1, 999999999999999), amount=course.price, **kwargs)
        user.balance = user.balance - course.price

        course.teacher.balance = course.teacher.balance + course.price
        
        user.save()    
        course.teacher.save()
        payment.save()

        return payment

