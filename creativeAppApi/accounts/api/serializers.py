from rest_framework import serializers
from rest_auth.registration.serializers import RegisterSerializer
from rest_auth.serializers import LoginSerializer
from django.contrib.auth import get_user_model
from accounts.models import Profile, Skill
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


#################### user following serializer ####################
# class UserFollowingSerializer(serializers.ModelSerializer):
#     '''
#     a user following serializer that gets the followers snd following
#     count, will also check if the user is already followed
#     '''
#     user = serializers.SlugRelatedField(read_only=True, slug_field='slug')
#     following_count = serializers.SerializerMethodField(read_only=True)
#     # followers_count = serializers.SerializerMethodField(read_only=True)
#     user_is_following = serializers.SerializerMethodField(read_only=True)
#     followed_on = serializers.SerializerMethodField(read_only=True)

#     class Meta:
#         model = UserFollowing
#         fields = "__all__"

#     def get_followed_on(self, instance):
#         return instance.followed_on.strftime("%d %B, %Y")

#     def get_following_count(self, instance):
#         return instance.following.count()

#     # def get_followers_count(self, instance):
#     #     return instance.followers.count()

#     def get_user_is_following(self, instance):
#         request = self.context.get("request")
#         return instance.following.filter(slug=request.user.slug).exists()

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

    class Meta:
        model = User
        fields = ('pk', 'email', 'fullname', 'profiles', 'slug')
        read_only_fields = ('email', 'fullname', 'profiles', 'slug')


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
