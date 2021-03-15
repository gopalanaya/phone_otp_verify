from rest_framework import serializers
from django.contrib.auth import get_user_model

from phone_verify.serializers import SMSVerificationSerializer

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'username','email']



class YourUserSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)
    first_name = serializers.CharField(default="First")
 

class CustomSerializer(UserSerializer, SMSVerificationSerializer):
    pass

