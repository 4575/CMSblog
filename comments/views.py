
from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.shortcuts import get_object_or_404

from posts.models import Post
from .models import Comment
from .serializers import CommentSerializer


class CommentListCreateView(generics.ListCreateAPIView):

    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Comment.objects.filter(
            post_id=self.kwargs['post_id'],
            is_approved=True,
            is_blocked=False
        )

    def perform_create(self, serializer):
        post = get_object_or_404(
            Post,
            id=self.kwargs['post_id'],
            is_published=True
        )

        serializer.save(
            user=self.request.user,
            post=post
        )
