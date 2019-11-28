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
                            ProfileSerializer, 
                            ProfileDetailedSerializer,
                            SkillSerializer)
from accounts.models import Profile, Skill


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
    permission_classes = [AllowAny]

    def get(self, request):
        user = get_user_model().objects.all()
        serializer = CustomUserDetailsSerializer(user, many=True)
        return Response(serializer.data)


class UserRetriveAPIView(generics.RetrieveAPIView):
    '''
    Gets a particular user in the database using the slug as the lookup
    '''
    queryset = get_user_model().objects.all()
    lookup_field = "slug"
    serializer_class = CustomUserDetailsSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsUserOrReadOnly]


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
    permission_classes = [IsAuthenticatedOrReadOnly, IsUserOrReadOnly]


############################### skill section ###############################
# Note: to be abel to add a skill by the superuser/AdminUser
# to also be able to get all skills in the data base

class SkillListAPIView(generics.ListCreateAPIView):
    '''
    gets all skills in the database
    '''
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    permission_classes = [IsAdminUserOrReadOnly]
