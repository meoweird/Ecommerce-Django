from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import ChangePasswordView, CustomerRegisterView, CustomerUpdateView, LogoutView


urlpatterns = [
    path('register', CustomerRegisterView.as_view(), name='register'),
    path('login', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh-token', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('update-profile', CustomerUpdateView.as_view(), name='update'),
    path('change-password', ChangePasswordView.as_view(), name='change-password'),
]
