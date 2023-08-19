from rest_framework import serializers

from bookmarks.models import Bookmark


class BookmarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookmark
        fields = "__all__"
        read_only_fields = (
            "created_at",
            "modified_at",
            "owner"
        )
