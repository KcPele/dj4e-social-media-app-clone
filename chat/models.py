from django.db import models
from accounts.models import User
# Create your models here.



class ChatMessage(models.Model):
    sender = models.ForeignKey(User, related_name='sender', on_delete=models.CASCADE)
    reciever = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.CharField(max_length=370, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.sender.username

class LikeMessage(models.Model):
    pass

class ReplyMessage(models.Model):
    pass

class ReactMessage(models.Model):
    pass