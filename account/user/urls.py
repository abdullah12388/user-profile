from django.urls import path, include
from .views import Login, Register, ForgetPassword, ResetPassword, UserProfile
from rest_framework import routers

router = routers.DefaultRouter()
router.register('register', Register, basename='register')

urlpatterns = [
    path('', include(router.urls)),
    path('login/', Login.as_view(), name='login'),
    path('forget-password/', ForgetPassword.as_view(), name='forget-password'),
    path('reset-password/', ResetPassword.as_view(), name='reset-password'),
    path('user/', UserProfile.as_view(), name='user')
]
