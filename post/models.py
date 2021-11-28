from django.db import models
from accounts.models import User
from django.urls import reverse_lazy
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class Post(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=170)
    body = models.TextField()
    #tag = models.ManyToManyField(Post, through='PostTag')
    image = models.ImageField(blank=True, null=True, upload_to='post')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse_lazy('post:post')
class Like(models.Model):
    post = models.ForeignKey(Post,  on_delete=models.CASCADE)
    liker = models.ForeignKey(User, on_delete=models.CASCADE)
    liked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.liker.username


class Comment(models.Model):
    body = models.TextField()
    post = models.ForeignKey(Post, related_name='comment',  on_delete=models.CASCADE)
    comment_user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.comment_user

class CommentLike(models.Model):
    comment = models.ForeignKey(Comment,  on_delete=models.CASCADE)
    commenter = models.ForeignKey(User, on_delete=models.CASCADE)
    commented_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return  self.commenter.username


##Not yet implemented
class CommentReply(models.Model):
    body = models.CharField(max_length=200, blank=True, null=True)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    reply_user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.comment_user

##not yet implemented
# class PostTag(models.Model):
      #title = models..CharField(max_length=48)  
#     post = models.ManyToManyField(Post, related_name='#tag')


###signals
# @receiver(post_save, sender=Post)
# def my_signal(sender, instance, created=True, **kwargs):
    
#     print(instance.title)
#     return 'nice'

