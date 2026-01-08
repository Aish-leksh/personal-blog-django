from django.db import models
from django.contrib.auth.models import User

from django.conf import settings

class Post(models.Model):
    CATEGORY_CHOICES = [
        ('Wellness', 'Wellness'),
        ('Lifestyle', 'Lifestyle'),
        ('Creative', 'Creative'),
        ('Fashion', 'Fashion'),
        ('Photography', 'Photography'),
        ('Time Management', 'Time Management'),
        ('Travel', 'Travel'),
    ]

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='posts/')
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def total_likes(self):
        return self.likes.count()



class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.post.title}'


class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('post', 'user')  # Prevent duplicate likes

    def __str__(self):
        return f'{self.user.username} likes {self.post.title}'

