from rest_framework import serializers
from rest_auth.registration.serializers import RegisterSerializer
from rest_auth.serializers import LoginSerializer
from django.contrib.auth import get_user_model
from accounts.models import Profile, Skill
from showcase.api.serializers import ShowcaseSlugSerializer
from datetime import date


#################### skills serializer ####################
class SkillSerializer(serializers.ModelSerializer):
    '''
    Allows people to view profile of people
    '''

    class Meta:
        model = Skill
        fields = ('name',)

        
#################### profile serializer ####################
class ProfileSerializer(serializers.ModelSerializer):
    '''
    Allows people to view profile of people
    '''
    skills = SkillSerializer(read_only=True, many=True)
    user = serializers.SlugRelatedField(read_only=True, slug_field='slug')

    class Meta:
        model = Profile
        fields = "__all__"

        read_only_fields = ('pk', 'user', 'skills')


class ProfileDetailedSerializer(serializers.ModelSerializer):
    '''
    gives a detailed description of the user, this ove would have 
    following, followers, and all info about the user
    '''
    skills = SkillSerializer(many=True, read_only=True)
    user = serializers.SlugRelatedField(read_only=True, slug_field='slug')
    age = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Profile
        fields = "__all__"

        read_only_fields = ('pk', 'user', 'skills')
    
    def get_age(self, instance):
        today = date.today()
        dob = instance.date_of_birth
        if dob==None:
            return None
        return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))


class ProfileSkillEditSerializer(serializers.ModelSerializer):
    '''
    For the user to edit his skill
    '''

    class Meta:
        model = Profile
        fields = ('skills',)


###################### user serializer ######################
User = get_user_model()

class LoginSerializer(LoginSerializer):
    '''
    a custom serializer that overides the default rest-auth, and for
    the user to not show username field when trying to login
    '''
    username = None


class CustomRegisterSerializer(RegisterSerializer):
    '''
    a custom serializer that overides the default rest-auth, and for
    the user to register himself
    '''
    username = None
    email = serializers.EmailField(required=True)
    password1 = serializers.CharField(write_only=True)
    fullname = serializers.CharField(required=True)
    slug = serializers.SlugField(read_only=True)

    def get_cleaned_data(self):
        super(CustomRegisterSerializer, self).get_cleaned_data()

        return {
            'password1': self.validated_data.get('password1', ''),
            'email': self.validated_data.get('email', ''),
            'fullname': self.validated_data.get('fullname', ''),
        }


class CustomUserDetailsSerializer(serializers.ModelSerializer):
    '''
    a custom serializer that overides the default rest-auth, and for
    the user to view his own data
    '''
    profiles = ProfileSerializer(read_only=True, many=True)
    slug = serializers.SlugField(read_only=True)
    showcase = ShowcaseSlugSerializer(read_only=True, many=True)

    class Meta:
        model = User
        fields = ('pk', 'email', 'fullname', 'profiles', 'slug', 'showcase')
        read_only_fields = ('email', 'fullname', 'profiles', 'slug', 'showcase')


class UserSerializer(serializers.ModelSerializer):
    '''
    a special serializer with not too much details,
    to chain to another serializer
    '''
    slug = serializers.SlugField(read_only=True)

    class Meta:
        model = User
        fields = ('pk', 'email', 'fullname', 'slug')
        read_only_fields = ('email', 'fullname', 'slug')
