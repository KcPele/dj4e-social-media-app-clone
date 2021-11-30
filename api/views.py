
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from accounts.models import (
    User,
    Follower,
    Friend
)

from post.models import (
    Post, 
    Comment,
    CommentLike,
)
from .permissions import (
    IsOwnerOrReadOnly, 
    IsCommentOwnerOrReadOnly,
    IsOwnerUserOrReadOnly,
)
from api.serializers import (
    UserCreationSerializer,
    PostSerializer, 
    UserSerializer,
    PasswordSerializer,
    CommentSerializer,
    CommentCreateSerializer,
)

# class AllApiRoute(APIView):
#     def get(self, request):
#         pass
#         routes = [
#             'GET: /api/',
#             'POST: /register/',
#             'POST: /token/',
#             'POST: /token/refresh/',
#             'GET: /users/',
#             'RETRIEVE, UPDATE: /users/id/',
#             'UPDATE: /users/id/change_password/',
#             'POST: /users/id/follow/',
#             'DELETE: /users/id/unfollow/',
#             'POST: /users/id/addfriend/',
           
#             'GET, POST: /posts/',
#             'RETRIEVE, UPDATE, DELETE: /posts/id/',
#             'POST: /posts/id/comment/',
#             'RETRIEVE, UPDATE, DELETE: /comments/id/',
#             'POST: /comment/id/likecomment/',
#             'POST: /comment/id/unlikecomment/',
            
            
#         ]
#         return Response(routes)

class CustomViewSet(viewsets.ViewSet):
    def list(self, request):
        serializer = self.serializer_class(self.queryset, many=True)
        return Response(serializer.data)
    def retrieve(self, request, pk=None):
        user = get_object_or_404(self.queryset, pk=pk)
        serializer = self.serializer_class(user)
        return Response(serializer.data)
    def update(self, request, pk=None):
        user = get_object_or_404(self.queryset, pk=pk)
        serializer = self.serializer_class(user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class UserViewSet(CustomViewSet):
    
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerUserOrReadOnly]
    

    #for user password change
    @action(detail=True, methods=['post'], url_path='change_password', 
    permission_classes=[permissions.IsAuthenticated, IsOwnerUserOrReadOnly])
    def set_password(self, request, pk=None):
        user = get_object_or_404(self.queryset, pk=pk)
        serializer = PasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user.set_password(serializer.validated_data['password'])
        user.save()
        return Response({'status':'password set'})
    
    ##for followers
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def follow(self, request, pk=None):
        follower = get_object_or_404(self.queryset, pk=pk)
        obj, created = Follower.objects.get_or_create(user=request.user)
        obj.followers.add(follower)
        return Response({'status':'you just followed ...'})

    #to unfollow 
    @action(detail=True, methods=['delete'], permission_classes=[permissions.IsAuthenticated])
    def unfollow(self, request, pk=None):
        follower = get_object_or_404(self.queryset, pk=pk)
        Follower.objects.get(user=request.user, followers=follower).delete()
        return Response({'status':'you unfollowed'})
    
    #adding a friend/ sending friend request
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def addfriend(self, request, pk=None):
        friend_user = get_object_or_404(self.queryset, pk=pk)
        obj, created = Friend.objects.get_or_create(owner=friend_user)
        obj.friends.add(request.user)
        return Response({'status':'now your friend'})




class CreateUserApi(generics.CreateAPIView):
    serializer_class = UserCreationSerializer
    def post(self, request):
        serializers = self.get_serializer(data=request.data)
        serializers.is_valid(raise_exception=True)
        serializers.save()
        return Response(serializers.data)


class PostViewSet(viewsets.ModelViewSet):
    
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)



    ##liking a post

    ##Unlike a post
    
    #creating comments for a post
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def comment(self, request, pk=None):
        post = get_object_or_404(self.queryset, pk=pk)
        comment_user = get_object_or_404(User, id=request.user.id)
        serializer = CommentCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        comment = Comment.objects.create(body=serializer.validated_data['body'],
         post=post, comment_user=comment_user)
        return Response({
            'comment': CommentSerializer(comment, 
            context=self.get_serializer_context()).data
            })




class CommentViewSet(CustomViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsCommentOwnerOrReadOnly]
    
    #like comments
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def likecomment(self, request, pk=None):
        com = get_object_or_404(self.queryset, id=pk)
        obj, created = CommentLike.objects.get_or_create(comment=com)
        obj.comment_liker.add(request.user)
        return Response({'status':'you just liked a comment'})
    
    #unlike a comment
