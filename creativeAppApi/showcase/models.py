from django.db import models
from django.conf import settings
from accounts.models import Skill


class Showcase(models.Model):
    '''
    Showcase model, that will have the works of the creatives,
    the key things here are the title, description, skilltype, 
    user posting it and content.

    people can like this showcases.
    '''
    title = models.CharField(max_length=500)
    description = models.TextField(null=True)
    skill_type = models.ForeignKey(Skill, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name="Showcases")
    content = models.TextField(null=True)
    created_on = models.DateTimeField(auto_now=True)
    updated_on = models.DateTimeField(auto_now_add=True)
    voters = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="upvotes")
    slug = models.SlugField(max_length=255, unique=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    '''
    Comment model, people will be able to comment on the showcase
    model above, and the comments can be upvoted
    '''
    post = models.ForeignKey(Showcase, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField(null=False)
    comment_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    comment_on = models.DateTimeField(auto_created=True)
    comment_voters = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="comment_upvotes")


# class CollaborationRequest(models.Model):
#     post = models.ForeignKey(Showcase, on_delete=models.CASCADE)
#     skill = models.ForeignKey(Skill, on_delete=models.CASCADE, null=True)
#     added_on = models.DateTimeField(null=True)

#     def __str__(self):
#         return self.post.name

