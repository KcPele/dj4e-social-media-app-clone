from rest_framework import serializers
from accounts.models import User, Follower
from post.models import Post, Comment, Like

from django.shortcuts import get_object_or_404


    
class UserSerializer(serializers.ModelSerializer):
    followers = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    friends = serializers.StringRelatedField(many=True, read_only=True)
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'name', 'bio', 
        'avater', 'date_of_birth', 'phone_number', 'gender', 'followers', 'friends']

class PasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=110, write_only=True)
    class Meta:
        fields = ['password']


class UserCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}
    
    def create(self, validate_date):
        user  = User.objects.create_user(username=validate_date['username'], 
        email=validate_date['email'], password=validate_date['password'])
        return user


class PostSerializer(serializers.ModelSerializer):
    comment = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    like = serializers.PrimaryKeyRelatedField(many=True, source='like.liker', read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'body', 'image', 'created_at', 'updated_at', 'is_deleted', 'owner', 'like', 'comment']
        extra_kwargs = {'owner':{'read_only': True}}
class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['body']
    

class CommentSerializer(serializers.ModelSerializer):
    commentlike = serializers.PrimaryKeyRelatedField(many=True, source='commentlike.comment_liker', read_only=True)
    class Meta:
        model = Comment
        fields = ['id', 'body', 'created_at','post', 'is_deleted', 'comment_user', 'commentlike']
        extra_kwargs = {'commentlike_set':{'read_only': True}, 'post':{'read_only': True}, 'comment_user': {'read_only': True}}