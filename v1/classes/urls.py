from django.urls import path
from rest_framework import routers
from . import views

app_name = "v1_classes"


router = routers.DefaultRouter()

router.register('course', views.CourseViewSet, basename="course")
router.register("payment", views.PaymentViewSet, basename="payment")


urlpatterns = []

urlpatterns += router.urls