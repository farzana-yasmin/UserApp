from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt
from rest_framework.routers import DefaultRouter
from api import views

router = DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
]