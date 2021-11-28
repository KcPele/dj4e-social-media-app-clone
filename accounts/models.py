from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse_lazy
class User(AbstractUser):
    GENDER_CHOICES =[
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    name = models.CharField(null=True, max_length=220)
    email = models.EmailField(unique=True, null=True)
    bio = models.TextField(null=True)
    avater = models.ImageField(null=True, default='default.png', upload_to='profile')
    date_of_birth = models.CharField(max_length=40, null=True)
    phone_number = models.IntegerField(null=True)
    gender = models.CharField(null=True, choices=GENDER_CHOICES, max_length=5)
    
    REQUIRED_FIELDS = []
    def __str__(self):
        return self.email
    
    def get_absolute_url(self):
        return reverse_lazy('profile', args=[self.id])
class Follower(models.Model):
    user = models.OneToOneField(User,  on_delete=models.CASCADE)
    followers = models.ManyToManyField(User, related_name='followers')

    def __str__(self):
        return self.user.username

class Friend(models.Model):
    owner = models.OneToOneField(User,  on_delete=models.CASCADE)
    friends = models.ManyToManyField(User, related_name='friends')

    def __str__(self):
        return self.owner.username


