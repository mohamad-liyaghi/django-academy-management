from django.urls import path, include
from rest_framework import routers
from djoser.views import UserViewSet
from rest_framework_simplejwt.views import TokenObtainPairView
from . import views

app_name = 'v1'

router = routers.SimpleRouter()

router.register('profile', views.ProfileViewSet)
router.register('request', views.RequestViewSet, basename="request")

register_user = UserViewSet.as_view({"post" : "create"})

urlpatterns = [
    path('register/', register_user, name="register"),
    path("login/", TokenObtainPairView.as_view(), name="login"),
    path('money/', views.get_money, name='get-money')
]

urlpatterns += router.urls