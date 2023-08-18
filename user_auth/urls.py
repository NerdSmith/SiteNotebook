from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView, TokenBlacklistView


jwt_urlpatterns = [
    path('jwt/create/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('jwt/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('jwt/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('jwt/blacklist/', TokenBlacklistView.as_view(), name='token_blacklist'),
]

urlpatterns = [

]

urlpatterns += jwt_urlpatterns
