from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import (
    # AllApiRoute,
    CreateUserApi,
    UserViewSet,

    ##post
    PostViewSet,
    CommentViewSet,
)

router = DefaultRouter()
router.register(r'posts', PostViewSet)
router.register(r'users', UserViewSet)
router.register(r'comments', CommentViewSet )


app_name = 'api'
urlpatterns = [
    # path('', AllApiRoute.as_view(), name='home'),
    path('register/', CreateUserApi.as_view(), name='register'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('', include(router.urls)),
]
