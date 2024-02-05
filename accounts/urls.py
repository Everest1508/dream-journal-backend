from django.contrib import admin
from django.urls import path,include
from .views import *

urlpatterns = [
    path('register/', RegisterAPIView.as_view()),
    # path('', include('accounts.urls')),
]