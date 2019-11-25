from rest_framework import serializers
from ..models import Showcase, Comment
from accounts.api.serializers import UserSerializer


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    created_at = serializers.SerializerMethodField(read_only=True)
    likes_count = serializers.SerializerMethodField(read_only=True)
    user_has_voted = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Comment
        exclude = ['showcase', 'voters', 'updated_at']

    def get_created_at(self, instance):
        return instance.created_at.strftime("%d %B, %Y")

    def get_likes_count(self, instance):
        return instance.voters.count()

    def get_user_has_voted(self, instance):
        request = self.context.get("request")
        return instance.voters.filter(pk=request.user.pk).exists()


class ShowcaseSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    created_on = serializers.SerializerMethodField(read_only=True)
    likes_count = serializers.SerializerMethodField(read_only=True)
    user_has_voted = serializers.SerializerMethodField(read_only=True)
    slug = serializers.SlugField(read_only=True)
    comment_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Showcase
        exclude = ['voters', 'updated_on']

    def get_created_on(self, instance):
        return instance.created_on.strftime("%d %B %Y")

    def get_likes_count(self, instance):
        return instance.voters.count()

    def get_user_has_voted(self, instance):
        request = self.context.get("request")
        return instance.voters.filter(pk=request.user.pk).exists()
    
    def get_comment_count(self, instance):
        return instance.comments.count()


class ShowcaseDetaiedSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    voters = UserSerializer(read_only=True, many=True)
    created_on = serializers.SerializerMethodField(read_only=True)
    likes_count = serializers.SerializerMethodField(read_only=True)
    user_has_voted = serializers.SerializerMethodField(read_only=True)
    slug = serializers.SlugField(read_only=True)
    comment_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Showcase
        exclude = ['updated_on',]

    def get_created_on(self, instance):
        return instance.created_on.strftime("%d %B %Y")

    def get_likes_count(self, instance):
        return instance.voters.count()

    def get_user_has_voted(self, instance):
        request = self.context.get("request")
        return instance.voters.filter(pk=request.user.pk).exists()
    
    def get_comment_count(self, instance):
        return instance.comments.count()