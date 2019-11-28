from django.urls import path
from django.conf.urls import url, include
from rest_auth.registration.views import VerifyEmailView
from rest_auth.views import (PasswordResetView, 
                            PasswordResetConfirmView)
from .views import (ConfirmEmailView, 
                    CustomRegisterView, 
                    FacebookLogin, 
                    GoogleLogin, 
                    ListUsersView,
                    UserRetriveAPIView,
                    ProfileRetriveUpdateAPIView,
                    SkillListAPIView)


urlpatterns = [
    path('verify-email/', VerifyEmailView.as_view(), name='account_email_verification_sent'),
    path('signup/account-confirm-email/<key>/', ConfirmEmailView.as_view(), name='account_confirm_email'),
    path('', include('rest_auth.urls')),
    path('signup/', include('rest_auth.registration.urls')),

    path('facebook/', FacebookLogin.as_view(), name='fb_login'),
    path('google/', GoogleLogin.as_view(), name='google_login'),

    path('password/reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password/reset/confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('users/', ListUsersView.as_view(), name='list-users'),
    path("users/<slug:slug>/", UserRetriveAPIView.as_view(), name="users-detail"),
    # To get the authenticated user's own object, its provided by djago-rest-auth using this route: 'rest-auth/user'
    path("profile/<int:pk>/", ProfileRetriveUpdateAPIView.as_view(), name="profile-detail"),
    path("skills/", SkillListAPIView.as_view(), name="skills"),
]