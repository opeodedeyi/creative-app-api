from django.conf import settings
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils.text import slugify

from core.utils import generate_user_string
from .models import Profile


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_profile(sender, instance, created, **kwargs):
    print("Created: ", created)
    if created:
        Profile.objects.create(user=instance)


@receiver(pre_save, sender=settings.AUTH_USER_MODEL)
def add_slug_to_user(sender, instance, *args, **kwargs):
    if instance and not instance.slug:
        slug = slugify(instance.fullname)
        slug_id = slugify(instance.id)
        random_string = generate_user_string()
        instance.slug = slug + "-" + random_string
        print(instance)