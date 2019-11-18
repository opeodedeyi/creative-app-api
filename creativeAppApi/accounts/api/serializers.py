from rest_framework import serializers
from rest_auth.registration.serializers import RegisterSerializer
from django.contrib.auth import get_user_model


class CustomRegisterSerializer(RegisterSerializer):

    email = serializers.EmailField(required=True)
    password1 = serializers.CharField(write_only=True)
    fullname = serializers.CharField(required=True)


    def get_cleaned_data(self):
        super(CustomRegisterSerializer, self).get_cleaned_data()

        return {
            'password1': self.validated_data.get('password1', ''),
            'email': self.validated_data.get('email', ''),
            'fullname': self.validated_data.get('fullname', ''),
        }

class CustomUserDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ('email','fullname')
        read_only_fields = ('email',)