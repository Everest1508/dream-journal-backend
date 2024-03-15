from django.shortcuts import render
from rest_framework.views import APIView
from django.core.mail import send_mail
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from .serializers import *
from .models import User
from rest_framework import status
from .utils import verify_email
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
import random
from django.contrib.auth import authenticate, login
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import smart_str

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'access': str(refresh.access_token),
        'refresh': str(refresh),
    }
    

class RegisterUserAPIView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        user = User.objects.filter(email=request.data['email']).first()
        if user:
            return Response({"msg":"User is already Registered"})

        if serializer.is_valid():
            user = serializer.save()

            # Generate OTP
            otp = random.randint(1000, 9999)
            user.otp = otp
            user.save()

            # Send OTP to the user's email
            send_mail(
                'Verification Code',
                f'Your verification code is {otp}',
                settings.EMAIL_HOST_USER,
                [user.email],
                fail_silently=False,
            )

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VerifyOTPAPIView(APIView):
    def post(self, request):
        email = request.data.get('email')
        otp = request.data.get('otp')

        try:
            user = User.objects.get(email=email)
            if user.otp == int(otp):
                user.is_trusty = True  
                user.save()
                return Response({'msg': 'Email verified successfully.'}, status=status.HTTP_200_OK)
            else:
                return Response({'msg': 'Invalid OTP.'}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({'msg': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        

class LoginUserAPIView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(email=email, password=password)
        if user and user.is_trusty:
            login(request, user)
            tokens = get_tokens_for_user(user)
            return Response(tokens)
        return Response({'msg': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)



class ForgotPasswordAPIView(APIView):
    def post(self, request):
        email = request.data.get('email')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'msg': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        
        reset_link = f"{settings.DOMAIN}/reset-password/{uid}/{token}/"
        
        send_mail(
            'Password Reset',
            f'Click the following link to reset your password: {reset_link}',
            settings.EMAIL_HOST_USER,
            [user.email],
            fail_silently=False,
        )
        
        return Response({'msg': 'Password reset link sent successfully','link':reset_link}, status=status.HTTP_200_OK)

class ResetPasswordAPIView(APIView):
    def post(self, request, uidb64, token):
        try:
            uid = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        
        if user is not None and default_token_generator.check_token(user, token):
            new_password = request.data.get('new_password')
            user.set_password(new_password)
            user.save()
            return Response({'msg': 'Password reset successful'}, status=status.HTTP_200_OK)
        else:
            return Response({'msg': 'Invalid password reset link'}, status=status.HTTP_400_BAD_REQUEST)
        