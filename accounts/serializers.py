from rest_framework import serializers
from .models import *
from django.utils import timezone

class MyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = "__all__"
        
    def create(self, validated_data):
        user = MyUser(
                        email=validated_data["email"],
                        full_name=validated_data["full_name"],
                        username=validated_data["username"]
                      )
        user.last_login = timezone.now()
        user.set_password(validated_data["password"])
        user.save()
        return user
    
class VerifySerializer(serializers.Serializer):
    username = serializers.CharField()
    otp = serializers.IntegerField()

    def validate(self, data):
        email = data.get('username')
        otp = data.get('otp')

        try:
            user = MyUser.objects.get(email=email, otp=otp, activated=False)
        except MyUser.DoesNotExist:
            raise serializers.ValidationError("Invalid email, OTP, or user is already activated.")

        return data