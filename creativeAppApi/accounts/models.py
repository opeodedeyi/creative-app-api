from django.contrib.auth.models import AbstractBaseUser,    BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
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
    

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['fullname']

    objects = UserManager()

    def __str__(self):
        return self.email


# class Skill(models.Model):
#     name = models.CharField(max_length=300)
#     created_on = models.DateTimeField(auto_now=True)
#     updated_on = models.DateTimeField(auto_now_add=True)
#     updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.DO_NOTHING)

#     def __str__(self):
#         return self.name


class Profile(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    age = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.user.fullname


# class Showcase(models.Model):
#     """Post model that would have the posts of the user"""
#     title = models.CharField(max_length=500)
#     description = models.TextField(null=True)
#     skill_type = models.ForeignKey("Skill", on_delete=models.CASCADE)
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
#     media = models.TextField(null=True)
#     created_on = models.DateTimeField(auto_now=True)
#     updated_on = models.DateTimeField(auto_now_add=True)
#     likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="like")

#     def __str__(self):
#         return self.title


# class CollaborationRequest(models.Model):
#     post = models.ForeignKey("Showcase", on_delete=models.CASCADE)
#     skill = models.ForeignKey("Skill", on_delete=models.CASCADE, null=True)
#     requested_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     requested_on = models.DateTimeField(auto_created=True)
#     approved = models.BooleanField(default=False, null=True)
#     approved_on = models.DateTimeField(null=True)

#     def __str__(self):
#         return self.post.name