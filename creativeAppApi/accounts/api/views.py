from rest_auth.registration.views import RegisterView
from django.contrib.auth import get_user_model
from rest_framework.generics import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.exceptions import NotFound
from rest_framework.views import APIView
from rest_framework.permissions import (AllowAny,
                                        IsAuthenticatedOrReadOnly, 
                                        IsAuthenticated, 
                                        IsAdminUser)

from .permissions import IsUserOrReadOnly, IsAdminUserOrReadOnly
from allauth.account.models import EmailConfirmation, EmailConfirmationHMAC
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from rest_auth.registration.views import SocialLoginView
from django.http import HttpResponseRedirect
from django.db.models import Q
from .serializers import (CustomUserDetailsSerializer,
                            UserSerializer,
                            ProfileSerializer, 
                            ProfileDetailedSerializer,
                            ProfileSkillEditSerializer,
                            SkillSerializer,
                            FollowerSerializer,
                            FollowingSerializer)
from showcase.api.serializers import ShowcaseSerializer
from showcase.models import Showcase
from accounts.models import Profile, Skill, FollowLog


############################### user authentication section ###############################
User = get_user_model()

class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter


class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter


class CustomRegisterView(RegisterView):
    '''
    a custom register view that overrides the rest-auth's default 
    '''
    permission_classes = [AllowAny]
    queryset = User.objects.all()


class ConfirmEmailView(APIView):
    '''
    a custom view that verifies the user email as the rest-auth default 
    solution doesnt work effectively
    From: https://gist.github.com/iMerica/a6a7efd80d49d6de82c7928140676957
    '''
    permission_classes = [AllowAny]

    def get(self, *args, **kwargs):
        self.object = confirmation = self.get_object()
        confirmation.confirm(self.request)
        # A React/Vue Router Route will handle the failure scenario
        return HttpResponseRedirect('/api/accounts/login/')

    def get_object(self, queryset=None):
        key = self.kwargs['key']
        email_confirmation = EmailConfirmationHMAC.from_key(key)
        if not email_confirmation:
            if queryset is None:
                queryset = self.get_queryset()
            try:
                email_confirmation = queryset.get(key=key.lower())
            except EmailConfirmation.DoesNotExist:
                # A React/Vue Router Route will handle the failure scenario
                return HttpResponseRedirect('/login/failure/')
        return email_confirmation

    def get_queryset(self):
        qs = EmailConfirmation.objects.all_valid()
        qs = qs.select_related("email_address__user")
        return qs


############################### Listing users in the database ###############################
class ListUsersView(APIView):
    '''
    Gets all the users in the database
    '''
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def get(self, request):
        user = get_user_model().objects.all()

        serializer_context = {"request": request}
        serializer = self.serializer_class(user, context=serializer_context, many=True)
        return Response(serializer.data)


class UserRetriveAPIView(APIView):
    '''
    Gets a particular user in the database using the slug as the lookup
    '''
    serializer_class = CustomUserDetailsSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsUserOrReadOnly]

    def get(self, request, slug):
        user = get_object_or_404(User, slug=slug)

        serializer_context = {"request": request}
        serializer = self.serializer_class(user, context=serializer_context)
        return Response(serializer.data, status=status.HTTP_200_OK)


############################### following and unfollowing users ###############################
class FollowAUserView(APIView):
    '''
    Follow a user
    '''
    permission_classes = [IsAuthenticated]

    def get(self, request, slug):
        response = {
            'status':None,
            'detail':None
        }
        response['status'],response['detail'] = request.user.follow_a_user(slug)
        return Response(response)


class UnFollowAUserView(APIView):
    '''
    unfollow a user
    '''
    permission_classes = [IsAuthenticated]

    def get(self, request, slug):
        response = {
            'status':None,
            'detail':None
        }
        response['status'],response['detail'] = request.user.unfollow_a_user(slug)
        return Response(response)


############################### Get followers and following ###############################
class UserFollowerView(APIView):
    '''
    Gets all the followers to a user
    '''
    permission_classes = [AllowAny]

    def get(self, request, slug):
        user = User.objects.get(slug=slug)
        followers = user.followers.all().filter(status='following').order_by("-followed_on")
        serializer = FollowerSerializer(followers, many=True)
        return Response(serializer.data)


class UserFollowingView(APIView):
    '''
    Gets all the users a user follows
    '''
    permission_classes = [AllowAny]

    def get(self, request, slug):
        user = User.objects.get(slug=slug)
        following = user.following.all().filter(status='following').order_by("-followed_on")
        serializer = FollowingSerializer(following, many=True)
        return Response(serializer.data)


############################### profile section ###############################

# Note: can get the profile PK from the user view and can edit the profile, or get
# a users detailed profile.

class ProfileRetriveUpdateAPIView(generics.RetrieveUpdateAPIView):
    '''
    gets a particular profile in the database and can edit
    if owned by the user
    '''
    queryset = Profile.objects.all()
    serializer_class = ProfileDetailedSerializer
    permission_classes = [IsUserOrReadOnly]


class ProfileSkillRUAPIView(generics.RetrieveUpdateAPIView):
    '''
    to edit the skills of the user alone
    '''
    queryset = Profile.objects.all()
    serializer_class = ProfileSkillEditSerializer
    permission_classes = [IsUserOrReadOnly]


############################### skill section ###############################
# Note: to be able to add a skill by the superuser/AdminUser
# to also be able to get all skills in the data base

class SkillListAPIView(generics.ListCreateAPIView):
    '''
    gets all skills in the database
    '''
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    permission_classes = [IsAdminUserOrReadOnly]


############################### get a users showcases ###############################
class ListAUsersShowcasesViewSet(generics.ListAPIView):
    '''
    List all the showcases of a user
    '''
    serializer_class = ShowcaseSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        kwarg_slug = self.kwargs.get("slug")
        user = get_object_or_404(User, slug=kwarg_slug)
        return Showcase.objects.filter(user=user)