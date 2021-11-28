from django.urls import path, include
from .views import (
    
    RegisterUser,
    ProfileUser,
    FollowUser,
    UnFollowUser,
    UpdateUser,
    AddFriend,
    AllFriends,
)   


urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('register/', RegisterUser.as_view(), name='register' ),
    path('profile/<str:pk>/', ProfileUser.as_view(), name="profile"),
    path('profile-update/<str:pk>/', UpdateUser.as_view(), name="profile_update"),
    path('follow/<str:pk>/', FollowUser.as_view(), name="follow"),
    path('unfollow/<str:pk>/', UnFollowUser.as_view(), name="unfollow"),
    path('friend/<str:pk>/', AddFriend.as_view(), name='add_friend'),
    path('allfriend/<str:pk>/', AllFriends.as_view(), name='all_friends'),
    
]
