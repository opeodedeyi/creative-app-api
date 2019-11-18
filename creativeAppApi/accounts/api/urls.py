from django.urls import path
from django.conf.urls import url, include
from rest_auth.registration.views import VerifyEmailView
from rest_auth.views import PasswordResetView, PasswordResetConfirmView
from .views import ConfirmEmailView, FacebookLogin, GoogleLogin


urlpatterns = [
    url(r'^verify-email/$', VerifyEmailView.as_view(), name='account_email_verification_sent'),
    url(r'^rest-auth/registration/account-confirm-email/(?P<key>[-:\w]+)/$', ConfirmEmailView.as_view(), name='account_confirm_email'),

    url('rest-auth/', include('rest_auth.urls')),
    url('rest-auth/registration/', include('rest_auth.registration.urls')),
    
    url('rest-auth/facebook/', FacebookLogin.as_view(), name='fb_login'),
    url('rest-auth/google/', GoogleLogin.as_view(), name='google_login'),

    url(r'^rest-auth/password/reset/$', PasswordResetView.as_view(), name='password_reset'),
    url(r'^rest-auth/password/reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
]