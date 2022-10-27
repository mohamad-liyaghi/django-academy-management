from django.urls import path, include
from rest_framework import routers
from . import views

app_name = 'v1'

router = routers.SimpleRouter()

router.register('', views.ProfileViewSet)


urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
]

urlpatterns += router.urls