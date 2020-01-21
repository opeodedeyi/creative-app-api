from django.conf.urls import include
from django.urls import path
from rest_auth.registration.views import VerifyEmailView
from rest_auth.views import (PasswordResetView,
                             PasswordResetConfirmView)

from .views import (ConfirmEmailView,
                    FacebookLogin,
                    GoogleLogin,
                    ListUsersView,
                    UserRetriveAPIView,
                    ProfileRetriveUpdateAPIView,
                    ProfileSkillRUAPIView,
                    SkillListAPIView,
                    FollowAUserView,
                    UnFollowAUserView,
                    UserFollowerView,
                    UserFollowingView,
                    ListAUsersShowcasesViewSet)

urlpatterns = [
     path('verify-email/', VerifyEmailView.as_view(), name='account_email_verification_sent'),
     path('signup/account-confirm-email/<key>/', ConfirmEmailView.as_view(), name='account_confirm_email'),
     path('', include('rest_auth.urls')),
     path('signup/', include('rest_auth.registration.urls')),
     path('facebook/', FacebookLogin.as_view(), name='fb_login'),
     path('google/', GoogleLogin.as_view(), name='google_login'),
     path('password/reset/', PasswordResetView.as_view(), name='password_reset'),
     path('password/reset/confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),

     # To get the authenticated user's own object, its provided by djago-rest-auth using this route: 'user/'
     path('users/', ListUsersView.as_view(), name='list-users'),
     path("users/<slug:slug>/", UserRetriveAPIView.as_view(), name="users-detail"),
     path("users/<slug:slug>/follow/", FollowAUserView.as_view(), name="users-follow"),
     path("users/<slug:slug>/unfollow/", UnFollowAUserView.as_view(), name="users-unfollow"),
     path("users/<slug:slug>/followers/", UserFollowerView.as_view(), name="user-followers"),
     path("users/<slug:slug>/following/", UserFollowingView.as_view(), name="user-following"),

     path("profile/<int:pk>/", ProfileRetriveUpdateAPIView.as_view(), name="profile-detail"),
     path("profile/<int:pk>/skills/", ProfileSkillRUAPIView.as_view(), name="profile-skill-edit"),
     path("skills/", SkillListAPIView.as_view(), name="skills"),

     # Querysets for users
     path("users/<slug:slug>/showcases/", ListAUsersShowcasesViewSet.as_view(), name="a-users-showcase-list"),
]
