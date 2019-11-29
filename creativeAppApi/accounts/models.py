from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
from datetime import date
from django.conf import settings


class UserManager(BaseUserManager):

  def _create_user(self, email, fullname, password, is_staff, is_superuser, **extra_fields):
    if not email:
        raise ValueError('Users must have an email address')
    now = timezone.now()
    email = self.normalize_email(email)
    fullname = fullname
    user = self.model(
        email=email,
        fullname=fullname,
        is_staff=is_staff, 
        is_active=True,
        is_superuser=is_superuser, 
        last_login=now,
        date_joined=now, 
        **extra_fields
    )
    user.set_password(password)
    user.save(using=self._db)
    return user

  def create_user(self, email, fullname, password, **extra_fields):
    return self._create_user(email, fullname, password, False, False, **extra_fields)

  def create_superuser(self, email, fullname, password, **extra_fields):
    user=self._create_user(email, fullname, password, True, True, **extra_fields)
    user.save(using=self._db)
    return user


class User(AbstractBaseUser, PermissionsMixin):
    username = None
    email = models.EmailField(max_length=254, unique=True)
    fullname = models.CharField(max_length=250)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['fullname']

    objects = UserManager()

    def __str__(self):
        return self.email


class Skill(models.Model):
    name = models.CharField(max_length=300)
    created_on = models.DateTimeField(auto_now=True)
    updated_on = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.name


SEX= (
    ('M', 'Male'),
    ('F', 'Female'),
)

BODYTYPE= (
    ('Slim', 'Slim'),
    ('Average', 'Average'),
    ('Athletic', 'Athletic'),
    ('Heavyset', 'Heavyset'),
)

class Profile(models.Model):
    '''
    Note:
    profile photo is expecting photos link gotten from cloudnairy from the frontend
    - The height is calculated in feets and inches
    - Need to sort out location (lives in)
    - Need to add an age function
    - Need to add achievemnet as a foreign field 
    - Need to add education also as a foreign field
    - Add follow functionality
    '''
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profiles')
    date_of_birth = models.DateField(blank=True, verbose_name="DOB", null=True)
    bio = models.TextField(max_length=500, blank=True, null=True)
    profile_photo = models.CharField(blank=True, max_length=300, null=True)
    skills = models.ManyToManyField(Skill, related_name='skills')
    sex = models.CharField(max_length=1, choices=SEX, blank=True, null=True)
    type_of_body = models.CharField(max_length=8, choices=BODYTYPE, blank=True, null=True)
    feet = models.PositiveIntegerField(blank=True, null=True)
    inches = models.PositiveIntegerField(blank=True, null=True)
    lives_in = models.CharField(max_length=50, blank=True, null=True)
    updated_on = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return self.user.fullname


class UserFollowing(models.Model):
    '''
    the created model shows info about when the person started following the user
    '''
    following = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="follows", null=False, blank=False, on_delete=models.DO_NOTHING)
    followers = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="followed_by", null=False, blank=False, on_delete=models.DO_NOTHING)
    created = models.DateTimeField(auto_now_add=True)