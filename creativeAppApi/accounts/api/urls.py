from django.conf.urls import include
from django.urls import path
from rest_auth.registration.views import VerifyEmailView
from rest_auth.views import (PasswordResetView,
                             PasswordResetConfirmView)
from allauth.account.views import ConfirmEmailView
from . import views as qv


urlpatterns = [
     path('verify-email/', VerifyEmailView.as_view(), name='account_email_verification_sent'),
     path('signup/account-confirm-email/<key>/', ConfirmEmailView.as_view(), name='account_confirm_email'),
     path('', include('rest_auth.urls')),
     path('signup/', include('rest_auth.registration.urls')),
     path('google/', qv.GoogleLogin.as_view(), name='google_login'),
     path('password/reset/', PasswordResetView.as_view(), name='password_reset'),
     path('password/reset/confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
     # path('resend_confirmation_email/', qv.EmailConfirmation.as_view(), name='resend-email-confirmation'),

     # To get the authenticated user's own object, its provided by djago-rest-auth using this route: 'user/'
     path('users/', qv.ListUsersView.as_view(), name='list-users'),
     path("users/<slug:slug>/", qv.UserRetriveAPIView.as_view(), name="users-detail"),
     path("users/<slug:slug>/follow/", qv.FollowAUserView.as_view(), name="users-follow"),
     path("users/<slug:slug>/unfollow/", qv.UnFollowAUserView.as_view(), name="users-unfollow"),
     path("users/<slug:slug>/followers/", qv.UserFollowerView.as_view(), name="user-followers"),
     path("users/<slug:slug>/following/", qv.UserFollowingView.as_view(), name="user-following"),

     path("profile/<int:pk>/", qv.ProfileRetriveUpdateAPIView.as_view(), name="profile-detail"),
     path("profile/<int:pk>/skills/", qv.ProfileSkillRUAPIView.as_view(), name="profile-skill-edit"),
     path("profile/<int:pk>/photo/", qv.ProfilePhotoRUAPIView.as_view(), name="profile-photo-edit"),
     path("skills/", qv.SkillListAPIView.as_view(), name="skills"),
     path("skillscreate/", qv.SkillCreateAPIView.as_view(), name="skills-create"),
     path("skills/<int:pk>/", qv.SkillUpdateAPIView.as_view(), name="skills-update-destroy"),

     # Querysets for users
     path("users/<slug:slug>/showcases/", qv.ListAUsersShowcasesViewSet.as_view(), name="a-users-showcase-list"),
]
