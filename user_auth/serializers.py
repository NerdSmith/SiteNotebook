from djoser.serializers import UserSerializer, UserCreateSerializer

from user_auth.models import User


class MyUserSerializer(UserSerializer):

    class Meta(UserSerializer.Meta):
        model = User
        fields = UserSerializer.Meta.fields + (
            "first_name",
            "last_name",
            "patronymic"
        )


class MyUserCreateSerializer(UserCreateSerializer, MyUserSerializer):
    class Meta:
        model = User
        fields = UserCreateSerializer.Meta.fields + MyUserSerializer.Meta.fields
