from rest_framework import serializers
from accounts.models import User, Follower
from post.models import Post, Comment

from django.shortcuts import get_object_or_404

class FollowerSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField()
    followers_id = serializers.IntegerField()
    class Meta:
        model = Follower
        fields = ['user_id', 'followers_id']
    
    def create(self, validate_date):
        user = get_object_or_404(User, id=validate_date['user_id'])
        follower = get_object_or_404(User, id=validate_date['followers_id'])
        obj, created = Follower.objects.get_or_create(user=user)
        obj.followers.add(follower)
        return obj
    
class UserSerializer(serializers.ModelSerializer):
    followers = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'followers']

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
    class Meta:
        model = Post
        fields = ['id', 'title', 'body', 'image', 'created_at', 'updated_at', 'like_set', 'comment']

class CommentCreateSerializer(serializers.ModelSerializer):
    post_id = serializers.IntegerField()
    comment_user_id = serializers.IntegerField(allow_null=True)
    class Meta:
        model = Comment
        fields = ['body', 'post_id', 'comment_user_id']
        read_only_fields = ['comment_user_id']
        

    def create(self, validata_data):
        post = get_object_or_404(Post, id=validata_data['post_id'])
        comment_user = get_object_or_404(User, id=validata_data['comment_user_id'])
        comment = Comment.objects.create(body=validata_data['body'], 
        post=post, comment_user=comment_user)
        return comment

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'body', 'created_at','post', 'comment_user', 'commentlike_set']
       
