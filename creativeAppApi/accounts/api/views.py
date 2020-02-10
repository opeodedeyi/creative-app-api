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
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from allauth.account.utils import send_email_confirmation
from rest_auth.registration.views import SocialLoginView
from django.http import HttpResponseRedirect
from django.db.models import Q
from .serializers import (CustomUserDetailsSerializer,
                            UserSerializer,
                            ProfileSerializer, 
                            ProfileDetailedSerializer,
                            ProfileSkillEditSerializer,
                            ProfilePhotoSerializer,
                            SkillSerializer,
                            FollowerSerializer,
                            FollowingSerializer)
from showcase.api.serializers import ShowcaseSerializer
from showcase.models import Showcase
from accounts.models import Profile, Skill, FollowLog


############################### user authentication section ###############################
User = get_user_model()

class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter


class CustomRegisterView(RegisterView):
    '''
    a custom register view that overrides the rest-auth's default 
    '''
    permission_classes = [AllowAny]
    queryset = User.objects.all()


############################# request new confirmation email #############################
# class EmailConfirmation(APIView):
#     permission_classes = [AllowAny] 

#     def post(self, request):
#         user = User.objects.get(email=request.data['email'] # the email sent from the client
        
#         # check if user exists or not, if user doesn't exist, send the response back to the user to let them know that no account with this email exists
#         # if user exists, resend the email using this

#         send_email_confirmation(request, request.user)
#         return Response({'message': 'Email confirmation sent'}, status=status.HTTP_201_CREATED)


############################## Listing users in the database ##############################
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

class ProfilePhotoRUAPIView(generics.RetrieveUpdateAPIView):
    '''
    to edit the photo of the user alone
    '''
    queryset = Profile.objects.all()
    serializer_class = ProfilePhotoSerializer
    permission_classes = [IsUserOrReadOnly]


############################### skill section ###############################
# Note: to be able to add a skill by the superuser/AdminUser
# to also be able to get all skills in the data base

class SkillListAPIView(generics.ListAPIView):
    '''
    gets all skills in the database
    '''
    serializer_class = SkillSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Skill.objects.all().order_by("subcategory")


class SkillCreateAPIView(generics.CreateAPIView):
    '''
    create a new skill in the database
    '''
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    permission_classes = [IsAdminUser]
    

class SkillUpdateAPIView(generics.RetrieveUpdateDestroyAPIView):
    '''
    update and delete a particular skill in the database
    '''
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    permission_classes = [IsAdminUser]


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