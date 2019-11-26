from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views as qv


urlpatterns = [
    path("", qv.showcaseCreateViewSet.as_view(), name="showcase-create"),
    path("<slug:slug>/", qv.showcaseRUDViewSet.as_view(), name="showcase-detail"),
    path("<slug:slug>/like/", qv.ShowcaseLikeAPIView.as_view(), name="showcase-like"),
    path("<slug:slug>/comment/", qv.CommentCreateAPIView.as_view(), name="comment-create"),
    path("<slug:slug>/comments/", qv.ShowcaseCommentListAPIView.as_view(), name="comment-list"),
    path("comments/<int:pk>/", qv.CommentRUDAPIView.as_view(), name="comment-detail"),
    path("comments/<int:pk>/like/", qv.CommentLikeAPIView.as_view(), name="comment-like"),
    path("comments/<int:pk>/reply/", qv.ReplyCreateAPIView.as_view(), name="reply-create"),
    path("comments/<int:pk>/replies/", qv.ReplyListAPIView.as_view(), name="reply-list"),
    path("replies/<int:pk>/", qv.ReplyRUDAPIView.as_view(), name="reply-detail"),
    path("replies/<int:pk>/like/", qv.ReplyLikeAPIView.as_view(), name="reply-like"),
]