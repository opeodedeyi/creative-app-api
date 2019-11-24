from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify

from core.utils import generate_random_string
from .models import Showcase