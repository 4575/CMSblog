from django.contrib.auth.models import User
from django.db import models

from posts.models import Post


# Create your models here.
class Comment(models.Model):

    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name="comments")

    user = models.ForeignKey(User,on_delete=models.CASCADE)


    content = models.TextField()

    is_approved = models.BooleanField(default=False)

    is_blocked = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.post.title}"