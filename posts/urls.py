from django.urls import path
from .views import LikePostView, toggle_like
from .views import (
    PostListCreateView,
    PostDetailView,
    home,
    post_detail_page
)
urlpatterns = [
    path('posts/', PostListCreateView.as_view(), name='post-list'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('', home, name='home'),
    path('blog/<int:id>/', post_detail_page, name='post-detail-page'),
    path(
    'posts/<int:post_id>/like/',
    LikePostView.as_view(),
    name='like-post'),
    path(
    'blog/<int:id>/like/',
    toggle_like,
    name='toggle-like'),
]