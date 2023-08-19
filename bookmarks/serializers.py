from drf_spectacular.utils import extend_schema_serializer
from rest_framework import serializers

from bookmarks.models import Bookmark


class BookmarkUrlSerializer(serializers.Serializer):
    target_url = serializers.URLField(max_length=2048, write_only=True, required=True)


class BookmarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookmark
        fields = "__all__"
