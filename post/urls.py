from django.conf import settings
from django.conf.urls.static import static


from django.urls import path
from post.views import (
    PostListView,
    PostCreateView,
    PostDetailView,
    PostUpdateView,
    PostDeleteView,
    LikeAddView,
    LikeDeleteView,
    #comment
    PostComment,
    DeleteComment,
    LikeCommentView,
    UnLikeCommentView,
    
)
app_name='post'
urlpatterns = [
    
    path('', PostListView.as_view(), name="post"),
    path('create/', PostCreateView.as_view(), name="create"),
    path('detail/<str:pk>/', PostDetailView.as_view(), name="detail"),
    path('update/<str:pk>/', PostUpdateView.as_view(), name="update"),
    path('delete/<str:pk>/', PostDeleteView.as_view(), name="delete"),

    ##likes
    path('like/', LikeAddView.as_view(), name='like'),
    path('unlike/', LikeDeleteView.as_view(), name='unlike'),

    ##comment
    path('post-comment/', PostComment.as_view(), name="comment"),
    path('delete-comment/<str:pk>/', DeleteComment.as_view(), name="delete_comment"),
    path('like-comment/', LikeCommentView.as_view(), name='like_comment'),
    path('unlike-comment/', UnLikeCommentView.as_view(), name='unlike_comment'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

