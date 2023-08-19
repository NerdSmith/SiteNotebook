from drf_spectacular.utils import extend_schema_serializer
from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault

from bookmarks.models import Bookmark, Collection


class BookmarkUrlSerializer(serializers.Serializer):
    target_url = serializers.URLField(max_length=2048, write_only=True, required=True)


class BookmarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookmark
        fields = "__all__"
        read_only_fields = ("owner", "link_type", "link")


class BookmarkCreateSerializer(serializers.ModelSerializer):
    class Meta(BookmarkSerializer.Meta):
        read_only_fields = []


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = "__all__"
        read_only_fields = ("owner", "bookmarks")


class CollectionCreateSerializer(CollectionSerializer):
    class Meta(CollectionSerializer.Meta):
        read_only_fields = ("bookmarks",)


class PrimaryKeyRelatedOwnerField(serializers.PrimaryKeyRelatedField):
    def get_queryset(self):
        user = self.context['request'].user
        queryset = super().get_queryset()
        if not user.is_staff:
            queryset = queryset.filter(owner=user.pk)
        return queryset


class BookmarkToCollectionSerializer(serializers.Serializer):
    bookmarks = PrimaryKeyRelatedOwnerField(
        required=True,
        many=True,
        queryset=Bookmark.objects.all(),
        source='authors_set'
    )


