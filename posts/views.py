from rest_framework import generics
from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response

from .models import Post
from .serializers import PostSerializer
from .permissions import IsAdminOrReadOnly

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status
from .models import Like
from django.shortcuts import redirect
from comments.models import Comment
from .models import Post, Like
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

class PostListCreateView(generics.ListCreateAPIView):

    serializer_class = PostSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Post.objects.all()

        return Post.objects.filter(is_published=True)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostDetailView(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = PostSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Post.objects.all()

        return Post.objects.filter(is_published=True)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        instance.views_count += 1
        instance.save(update_fields=['views_count'])

        serializer = self.get_serializer(instance)
        return Response(serializer.data)




def home(request):
    posts = Post.objects.filter(is_published=True).order_by('-created_at')
    return render(request, 'posts/home.html', {'posts': posts})




def post_detail_page(request, id):
    post = get_object_or_404(
        Post,
        id=id,
        is_published=True
    )

    if request.method == 'POST' and request.user.is_authenticated:
        content = request.POST.get('content')

        if content:
            Comment.objects.create(
                post=post,
                user=request.user,
                content=content
            )

        return redirect('post-detail-page', id=id)

    post.views_count += 1
    post.save(update_fields=['views_count'])

    comments = post.comments.filter(
        is_approved=True,
        is_blocked=False
    )

    likes_count = post.likes.count()

    user_has_liked = False

    if request.user.is_authenticated:
        user_has_liked = post.likes.filter(
            user=request.user
        ).exists()

    return render(request, 'posts/detail.html', {
        'post': post,
        'comments': comments,
        'likes_count': likes_count,
        'user_has_liked': user_has_liked
    })




class LikePostView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, post_id):
        post = get_object_or_404(
            Post,
            id=post_id,
            is_published=True
        )

        Like.objects.get_or_create(
            post=post,
            user=request.user
        )

        return Response({
            'message': 'Post liked successfully',
            'likes_count': post.likes.count()
        })

    def delete(self, request, post_id):
        post = get_object_or_404(
            Post,
            id=post_id,
            is_published=True
        )

        Like.objects.filter(
            post=post,
            user=request.user
        ).delete()

        return Response({
            'message': 'Like removed successfully',
            'likes_count': post.likes.count()
        })



@login_required
@require_POST
def toggle_like(request, id):
    post = get_object_or_404(Post, id=id)

    like, created = Like.objects.get_or_create(
        post=post,
        user=request.user
    )

    if not created:
        like.delete()

    return redirect('post-detail-page', id=id)