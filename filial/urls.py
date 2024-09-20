from django.urls import path, include
from filial.views import FilialViewSet
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'filial', FilialViewSet, basename='filial')


urlpatterns = [
    path('', include(router.urls)),
]