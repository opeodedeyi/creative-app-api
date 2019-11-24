from django.db import models
from django.conf import settings
from accounts.models import Skill


# class Showcase(models.Model):
#     """Post model that would have the posts of the user"""
#     title = models.CharField(max_length=500)
#     description = models.TextField(null=True)
#     skill_type = models.ForeignKey("Skill", on_delete=models.CASCADE)
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
#     media = models.TextField(null=True)
#     created_on = models.DateTimeField(auto_now=True)
#     updated_on = models.DateTimeField(auto_now_add=True)
#     liked = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="liked")

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