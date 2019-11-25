from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views as qv

router = DefaultRouter()
router.register(r"showcase", qv.ShowcaseViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("showcase/<slug:slug>/comment/", qv.CommentCreateAPIView.as_view(), name="comment-create"),
    path("showcase/<slug:slug>/comments/", qv.ShowcaseCommentListAPIView.as_view(), name="comment-list"),
    path("comments/<int:pk>/", qv.CommentRUDAPIView.as_view(), name="comment-detail"),
    path("comments/<int:pk>/like/", qv.CommentLikeAPIView.as_view(), name="comment-like"),
]