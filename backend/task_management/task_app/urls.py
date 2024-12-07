from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'create', RegisterViewSet, basename='createuser')
router.register(r'login', LoginViewSet, basename='loginuser')


urlpatterns = [
    path('', include(router.urls)),
]