
from rest_framework import serializers
from .models import Comment


class CommentSerializer(serializers.ModelSerializer):

    username = serializers.CharField(
        source='user.username',
        read_only=True
    )

    class Meta:
        model = Comment
        fields = [
            'id',
            'post',
            'user',
            'username',
            'content',
            'is_approved',
            'is_blocked',
            'created_at'
        ]

        read_only_fields = [
            'user',
            'username',
            'is_approved',
            'is_blocked',
            'created_at'
        ]
