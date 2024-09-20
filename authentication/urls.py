from django.urls import path, include
from authentication.views import CustomUserViewSet, MyTokenObtainPairView, FuncaoViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'user', CustomUserViewSet)
router.register(r'funcao', FuncaoViewSet)

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

urlpatterns = [
    path('', include(router.urls)),
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]