from django.shortcuts import render
from rest_framework.views import APIView
# Create your views here.
from django.core.mail import send_mail
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from .serializers import *
from .models import MyUser
from rest_framework import status
from .utils import verify_email

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
    

class RegisterAPIView(APIView):
    def post(self,request):
        serializer = MyUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        tokens = get_tokens_for_user(user)
        verify_email(email=user.email,otp=user.otp)
        print(user.otp)
        return Response({
            "tokens": tokens,
            "message": "User registered successfully.",
        }, status=status.HTTP_201_CREATED)
        