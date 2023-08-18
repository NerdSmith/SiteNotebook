from django.urls import path
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView, TokenBlacklistView

from user_auth.views import UserViewSet

jwt_urlpatterns = [
    path('jwt/create/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('jwt/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('jwt/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('jwt/blacklist/', TokenBlacklistView.as_view(), name='token_blacklist'),
]

user_router = SimpleRouter()
user_router.register("auth/user", UserViewSet, basename="users")

urlpatterns = []

urlpatterns += jwt_urlpatterns
urlpatterns += user_router.urls
