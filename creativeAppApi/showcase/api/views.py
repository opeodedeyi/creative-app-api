from rest_framework import generics, viewsets, status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from .permissions import IsUserOrReadOnly
from .serializers import ShowcaseSerializer, CommentSerializer, ShowcaseDetaiedSerializer
from ..models import Showcase, Comment


class showcaseCreateViewSet(generics.ListCreateAPIView):
    queryset = Showcase.objects.all()
    serializer_class = ShowcaseSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class showcaseRUDViewSet(generics.RetrieveUpdateDestroyAPIView):
    queryset = Showcase.objects.all()
    lookup_field = "slug"
    serializer_class = ShowcaseDetaiedSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsUserOrReadOnly]


class ShowcaseLikeAPIView(APIView):
    serializer_class = ShowcaseDetaiedSerializer
    permission_classes = [IsAuthenticated]

    def delete(self, request, slug):
        showcase = get_object_or_404(Showcase, slug=slug)
        user = self.request.user

        showcase.voters.remove(user)
        showcase.save()

        serializer_context = {"request": request}
        serializer = self.serializer_class(showcase, context=serializer_context)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, slug):
        showcase = get_object_or_404(Showcase, slug=slug)
        user = self.request.user

        showcase.voters.add(user)
        showcase.save()

        serializer_context = {"request": request}
        serializer = self.serializer_class(showcase, context=serializer_context)

        return Response(serializer.data, status=status.HTTP_200_OK)


class CommentCreateAPIView(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        request_user = self.request.user
        kwargs_slug = self.kwargs.get("slug")
        showcase = get_object_or_404(Showcase, slug=kwargs_slug)

        serializer.save(user=request_user, showcase=showcase)


class CommentRUDAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsUserOrReadOnly]


class ShowcaseCommentListAPIView(generics.ListAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        kwarg_slug = self.kwargs.get("slug")
        return Comment.objects.filter(showcase__slug=kwarg_slug).order_by("-created_at")


class CommentLikeAPIView(APIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        user = self.request.user

        comment.voters.remove(user)
        comment.save()

        serializer_context = {"request": request}
        serializer = self.serializer_class(comment, context=serializer_context)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        user = self.request.user

        comment.voters.add(user)
        comment.save()

        serializer_context = {"request": request}
        serializer = self.serializer_class(comment, context=serializer_context)

        return Response(serializer.data, status=status.HTTP_200_OK)
