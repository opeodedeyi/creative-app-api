from rest_auth.registration.views import RegisterView
from django.contrib.auth import get_user_model
from rest_framework.generics import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.exceptions import NotFound
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly, IsAuthenticated, IsAdminUser
from allauth.account.models import EmailConfirmation, EmailConfirmationHMAC
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from rest_auth.registration.views import SocialLoginView
from django.http import HttpResponseRedirect
from django.db.models import Q
from .serializers import CustomUserDetailsSerializer, ProfileSerializer
from accounts.models import Profile


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
    queryset = User.objects.all()


class ConfirmEmailView(APIView):
    '''
    a custom view that verifies the user email as the rest-auth default 
    solution doesnt work effectively
    '''
    permission_classes = [AllowAny]

    def get(self, *args, **kwargs):
        self.object = confirmation = self.get_object()
        confirmation.confirm(self.request)
        # A React/Vue Router Route will handle the failure scenario
        return HttpResponseRedirect('/api/accounts/rest-auth/login/')

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


############################### Listing usersin the database ###############################
class ListUsersView(APIView):
    '''
    Gets all the users in the database
    '''
    permission_classes = [AllowAny]

    def get(self, request):
        user = User.objects.all()
        serializer = CustomUserDetailsSerializer(user, many=True)
        return Response(serializer.data)


class UserDetailAPIView(APIView):
    '''
    Gets a particular user in the database
    '''
    permission_classes = [AllowAny]

    def get_object(self, pk):
        user = get_object_or_404(User, pk=pk)
        return user

    def get(self, request, pk):
        user = self.get_object(pk)
        serializer = CustomUserDetailsSerializer(user)
        return Response(serializer.data)


############################### profile section ###############################

# Note: there is no need to be able to get all profiles, this is just for test purpose
# i.e. ProfileListAPIView is irrelevant

class ProfileListAPIView(APIView):
    '''
    gets all the profiles in the database
    '''
    def get(self, request):
        profile = Profile.objects.all()
        serializer = ProfileSerializer(profile, many=True)
        return Response(serializer.data)


class ProfileDetailAPIView(APIView):
    '''
    gets a particular profile in the database and can edit
    TO-Do:
    customize the permission to is object owner or read only
    '''
    permission_classes = [IsAuthenticated]


    def get_object(self, pk):
        profile = get_object_or_404(Profile, pk=pk)
        return profile

    def get(self, request, pk):
        profile = self.get_object(pk)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

    def put(self, request, pk):
        profile = self.get_object(pk)
        serializer = ProfileSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
