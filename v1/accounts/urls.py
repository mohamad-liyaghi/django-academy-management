from django.urls import path, include
from rest_framework import routers
from . import views

app_name = 'v1'

router = routers.SimpleRouter()

router.register('profile', views.ProfileViewSet)
router.register('request', views.RequestViewSet, basename="request")


urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('money/', views.get_money, name='get-money')
]

urlpatterns += router.urls