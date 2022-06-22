from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Post(models.Model):

    user = models.ForeignKey(User,on_delete=models.CASCADE)
    body = models.CharField(max_length=500)
    slug = models.SlugField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return ' ' + self.slug + '' + str(self.updated)

    def get_absolute_path(self):
        return reverse('home:detail', args=[self.id, self.slug])

    def like_count(self):
        return self.posts_like.count()


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ucomments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='pcomments')
    body = models.TextField(max_length=400)
    created = models.DateTimeField(auto_now_add=True)
    reply = models.ForeignKey('self', on_delete=models.CASCADE, related_name='creply', blank=True, null=True)
    is_reply = models.BooleanField(default=False)


class Like(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE, related_name='user_likes')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='posts_like')






