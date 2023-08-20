from djoser.conf import settings
from djoser.permissions import CurrentUserOrAdmin
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet

from user_auth.models import User
from user_auth.serializers import MyUserSerializer, MyUserCreateSerializer


@extend_schema_view(
    list=extend_schema(description='Lists all users. Returns only current user for no-admin user.'),
    create=extend_schema(description='Creates a new user'),
    retrieve=extend_schema(description='Gets user by id.'),
    update=extend_schema(description='Updates user by id.'),
    partial_update=extend_schema(description='Updates user by id. (Partial)'),
    destroy=extend_schema(description='Deletes user by id.'),
)
class UserViewSet(ModelViewSet):
    serializer_class = MyUserSerializer
    queryset = User.objects.all()
    permission_classes = [CurrentUserOrAdmin, ]

    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset()
        if settings.HIDE_USERS and self.action == "list" and not user.is_staff:
            queryset = queryset.filter(pk=user.pk)
        return queryset

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [AllowAny, ]
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action == 'create':
            self.serializer_class = MyUserCreateSerializer
        return super().get_serializer_class()
