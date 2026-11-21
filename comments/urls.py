
from django.urls import path
from .views import CommentListCreateView

urlpatterns = [
    path(
        'posts/<int:post_id>/',
        CommentListCreateView.as_view(),
        name='comment-list-create'
    ),
]
