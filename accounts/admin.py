from django.contrib import admin

from django.contrib.auth.admin import UserAdmin
from .models import User, Follower, Friend

admin.site.register(User)
admin.site.register(Follower)
admin.site.register(Friend)