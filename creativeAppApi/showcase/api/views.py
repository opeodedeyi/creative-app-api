from django.contrib.auth import get_user_model
from rest_framework import generics, viewsets, status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny

from .permissions import IsUserOrReadOnly
from .serializers import ShowcaseSerializer, CommentSerializer, ShowcaseDetaiedSerializer, ReplySerializer
from ..models import Showcase, Comment, ReplyComment


User = get_user_model()
# SHOWCASE APIView
class showcaseListCreateViewSet(generics.ListCreateAPIView):
    '''
    Create list and showcases view. user must be logged in to do this
    '''
    queryset = Showcase.objects.all()
    serializer_class = ShowcaseSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class showcaseRUDViewSet(generics.RetrieveUpdateDestroyAPIView):
    '''
    Retrieve, update and destroy showcases view. user must be 
    owner of the object to be able to destroy and update
    '''
    queryset = Showcase.objects.all()
    lookup_field = "slug"
    serializer_class = ShowcaseDetaiedSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsUserOrReadOnly]


class ShowcaseLikeAPIView(APIView):
    '''
    Can like(post) and unlike(delete) the showcases, must be 
    authenticated to do this
    '''
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


# COMMENT APIView
class CommentCreateAPIView(generics.CreateAPIView):
    '''
    Can comment on showcases view. user must be 
    authenticated to do this
    '''
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        request_user = self.request.user
        kwargs_slug = self.kwargs.get("slug")
        showcase = get_object_or_404(Showcase, slug=kwargs_slug)

        serializer.save(user=request_user, showcase=showcase)


class CommentRUDAPIView(generics.RetrieveUpdateDestroyAPIView):
    '''
    Can edit and delete  the comment, the user must be owner of 
    the object to do this
    '''
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsUserOrReadOnly]


class ShowcaseCommentListAPIView(generics.ListAPIView):
    '''
    Can see all the comments related to a particular showcase, 
    the user must be authenticated to do this
    '''
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        kwarg_slug = self.kwargs.get("slug")
        return Comment.objects.filter(showcase__slug=kwarg_slug).order_by("-created_at")


class CommentLikeAPIView(APIView):
    '''
    Can like(post) and unlike(delete) the comments, must be 
    authenticated to do this
    '''
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


# REPLY APIView
class ReplyCreateAPIView(generics.CreateAPIView):
    '''
    Can reply on comment view. user must be 
    authenticated to do this
    '''
    queryset = ReplyComment.objects.all()
    serializer_class = ReplySerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        request_user = self.request.user
        kwargs_pk = self.kwargs.get("pk")
        comment = get_object_or_404(Comment, pk=kwargs_pk)

        serializer.save(user=request_user, comment=comment)


class ReplyRUDAPIView(generics.RetrieveUpdateDestroyAPIView):
    '''
    Can edit and delete  the reply, the user must be owner of 
    the object to do this
    '''
    queryset = ReplyComment.objects.all()
    serializer_class = ReplySerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsUserOrReadOnly]


class ReplyListAPIView(generics.ListAPIView):
    '''
    Can see all the replies related to a particular comment, 
    the user must be authenticated to do this
    '''
    serializer_class = ReplySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        kwarg_pk = self.kwargs.get("pk")
        return ReplyComment.objects.filter(comment__pk=kwarg_pk).order_by("-created_at")


class ReplyLikeAPIView(APIView):
    '''
    Can like(post) and unlike(delete) the reply, must be 
    authenticated to do this
    '''
    serializer_class = ReplySerializer
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        reply = get_object_or_404(ReplyComment, pk=pk)
        user = self.request.user

        reply.voters.remove(user)
        reply.save()

        serializer_context = {"request": request}
        serializer = self.serializer_class(reply, context=serializer_context)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, pk):
        reply = get_object_or_404(ReplyComment, pk=pk)
        user = self.request.user

        reply.voters.add(user)
        reply.save()

        serializer_context = {"request": request}
        serializer = self.serializer_class(reply, context=serializer_context)

        return Response(serializer.data, status=status.HTTP_200_OK)