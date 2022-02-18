from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


class User(AbstractUser):
    pass


class Post(models.Model):
    content = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="post")
    timestamp = models.DateTimeField(auto_now_add=True)

    def serialize(self):
        return {
        "id": self.id,
        "content": self.content,
        "author": self.author.username,
        "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p")
        }


    def __str__(self):
        return f"{self.content}"


class Follow(models.Model):
    # User that will actively follow
    follower = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="follower")
    # Person that the user is following
    following = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="following")

    def __str__(self):
        return f"{self.follower} is following {self.following}"

class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post")
    like_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="like_user")




