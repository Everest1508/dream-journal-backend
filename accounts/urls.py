from django.contrib import admin
from django.urls import path,include
from .views import *

urlpatterns = [
    path('register/',RegisterUserAPIView.as_view()),
    path('verify/',VerifyOTPAPIView.as_view()),
    path('login/',LoginUserAPIView.as_view()),
    # path('myprofile/',UserProfileAPIView.as_view()),
    path('forgot-password/', ForgotPasswordAPIView.as_view(), name='forgot_password'),
    path('reset-password/<str:uidb64>/<str:token>/', ResetPasswordAPIView.as_view(), name='reset_password'),
]