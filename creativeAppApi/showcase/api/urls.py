from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views as qv


urlpatterns = [
    path("create/", qv.showcaseCreateViewSet.as_view(), name="showcase-create"),
    path("list/", qv.showcaseListViewSet.as_view(), name="showcase-list-create"),
    path("mostliked/", qv.MostLikedShowcasesView.as_view(), name="most-liked-showcases"),
    path("mostlikedy/", qv.MostLikedYearShowcasesView.as_view(), name="most-liked-showcases-year"),
    path("mostlikedm/", qv.MostLikedMonthShowcasesView.as_view(), name="most-liked-showcases-month"),
    path("mostlikedw/", qv.MostLikedWeekShowcasesView.as_view(), name="most-liked-showcases-week"),
    path("followingshowcases/", qv.FollowingShowcasesView.as_view(), name="followed-users-showcases"),
    path("<slug:slug>/", qv.showcaseRUDViewSet.as_view(), name="showcase-detail"),
    path("<slug:slug>/like/", qv.ShowcaseLikeAPIView.as_view(), name="showcase-like"),
    path("<slug:slug>/comment/", qv.CommentCreateAPIView.as_view(), name="comment-create"),
    path("<slug:slug>/comments/", qv.ShowcaseCommentListAPIView.as_view(), name="comment-list"),
    # path("<slug:slug>/collaborator/create", qv.ShowcaseCommentListAPIView.as_view(), name="add-collaborator-to-showcase"),
    path("comments/<int:pk>/", qv.CommentRUDAPIView.as_view(), name="comment-detail"),
    path("comments/<int:pk>/like/", qv.CommentLikeAPIView.as_view(), name="comment-like"),
    path("comments/<int:pk>/reply/", qv.ReplyCreateAPIView.as_view(), name="reply-create"),
    path("comments/<int:pk>/replies/", qv.ReplyListAPIView.as_view(), name="reply-list"),
    path("replies/<int:pk>/", qv.ReplyRUDAPIView.as_view(), name="reply-detail"),
    path("replies/<int:pk>/like/", qv.ReplyLikeAPIView.as_view(), name="reply-like"),
]