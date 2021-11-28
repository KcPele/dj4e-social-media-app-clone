
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import status
from rest_framework.views import APIView
from accounts.models import (
    User,
    Follower,
)
from post.models import Post, Comment
from .permissions import IsOwnerOrReadOnly, IsCommentOwnerOrReadOnly
from api.serializers import (
    UserCreationSerializer,
    PostSerializer, 
    UserSerializer,
    FollowerSerializer,
    CommentSerializer,
    CommentCreateSerializer,
)

class AllApiRoute(APIView):
    def get(self, request):
        routes = [
            'GET: /api/',
            'POST: /register/',
            'POST: /token/',
            'POST: /token/refresh/',
            'GET: /users/',
            'GET: /users/id/',
            'RETRIEVE, UPDATE: /profile/id/',
            'GET, POST: /followers/id/',
           
            'GET, POST: /posts/',
            'RETRIEVE, DELETE, UPDATE: /posts/id/',
            'POST: /create-comments/',
            'RETRIEVE, DELETE, UPDATE: /comments/id/',
            'POST: /like_comment/',
            
            
        ]
        return Response(routes)
   
class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class CreateUserApi(generics.CreateAPIView):
    serializer_class = UserCreationSerializer
    def post(self, request):
        serializers = self.get_serializer(data=request.data)
        serializers.is_valid(raise_exception=True)
        serializers.save()
        return Response(serializers.data)

class FollowerCreateView(generics.CreateAPIView):
    serializer_class = FollowerSerializer
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

class CommentCreateView(generics.CreateAPIView):
    
    serializer_class = CommentCreateSerializer
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        data = request.data
        
        
        serializers = self.get_serializer(data=request.data)
       
        serializers.is_valid(raise_exception=True)
        print(serializers)
        serializers.save(comment_user_id=request.user.id)
        return Response(serializers.data)

class CommentViewSet(viewsets.ModelViewSet):
    
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsCommentOwnerOrReadOnly]
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
