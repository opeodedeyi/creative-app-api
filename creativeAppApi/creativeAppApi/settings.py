import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'ajw*zrcim60xjdy0#9_g6$&t!iu%&i)@gu_gf8l#1(6a@!$$t!'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1']


# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.sites',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'rest_auth',
    'rest_auth.registration',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.facebook',
    'accounts',
    'showcase',
    'collaborate',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'creativeAppApi.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'creativeAppApi.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'email',
            'profile',
            'name'
        ],
        'AUTH_PARAMS': {
            'access_type': 'offline',
        },
        'APP': {
            # get from "console.developers.google.com/" then apis then credentials then oauthclient
            # fill in http://127.0.0.1:8000/accounts/google/login/callback/ in the “Authorized redirect URI” field
            'client_id': '63645136767-t0aqhv7ieuo7raf5lcsos2j5q3rsvr6c.apps.googleusercontent.com',
            'secret': 'jA5tysVYG6_3Tm5DsvWz8BgL',
            'key': ''
        }
    }
}

# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Africa/Niamey'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'creativeAppApi/static')
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ]
}

AUTH_USER_MODEL = 'accounts.User'

SITE_ID = 1

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

# restauth old password field required when changing password enabled
OLD_PASSWORD_FIELD_ENABLED = True
# allauth and rest auth logout on pasword change disabled
ACCOUNT_LOGOUT_ON_PASSWORD_CHANGE = False
LOGOUT_ON_PASSWORD_CHANGE = False
# alluth user model extension settings
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_USER_EMAIL_FIELD = 'email'
ACCOUNT_USER_MODEL_EMAIL_FIELD = "email"
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_SESSION_REMEMBER = True
# allauth logout on get enabled
ACCOUNT_LOGOUT_ON_GET = True
# verification of email is compulsory/mandatory
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
# allauth confirm email on get (to be changed later)
ACCOUNT_CONFIRM_EMAIL_ON_GET = True
# login redirect
ACCOUNT_AUTHENTICATED_LOGIN_REDIRECTS =True
LOGIN_URL = "api/login/"
LOGIN_REDIRECT_URL = "/"
ACCOUNT_LOGOUT_REDIRECT_URL = "/"
ACCOUNT_EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL = "api/authsuccess"
# once email is confirmed login the user, only works if signed up not long ago
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = False
# days in which the confirmation email will expire
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 2
# not sure bitr important
ACCOUNT_EMAIL_CONFIRMATION_HMAC =True
# when user tries to login and fails the limit conssecutively, 
# the timeout befor trying again, timeout measured in seconds
ACCOUNT_LOGIN_ATTEMPTS_LIMIT = 5
ACCOUNT_LOGIN_ATTEMPTS_TIMEOUT = 60
# social media verification important
SOCIALACCOUNT_EMAIL_VERIFICATION = 'mandatory'
# social media email important
SOCIALACCOUNT_EMAIL_REQUIRED = ACCOUNT_EMAIL_REQUIRED
 
# Email SMPT settings
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'opedoetester@gmail.com'
EMAIL_HOST_PASSWORD = '9ja4lifE'
DEFAULT_FROM_EMAIL = 'opedoetester@gmail.com'
DEFAULT_TO_EMAIL = EMAIL_HOST_USER

# rest auth serializers
REST_AUTH_SERIALIZERS = {
    "USER_DETAILS_SERIALIZER": "accounts.api.serializers.CustomUserDetailsSerializer",
    'LOGIN_SERIALIZER': 'accounts.api.serializers.LoginSerializer',
    'PASSWORD_RESET_SERIALIZER': 'accounts.api.serializers.PasswordResetSerializer',
}

REST_AUTH_REGISTER_SERIALIZERS = {
    "REGISTER_SERIALIZER": "accounts.api.serializers.CustomRegisterSerializer",
}

ACCOUNT_ADAPTER = 'accounts.adapters.CustomUserAccountAdapter'
