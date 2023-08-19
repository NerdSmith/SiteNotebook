from djoser.permissions import CurrentUserOrAdmin
from rest_framework import viewsets, mixins
from rest_framework.response import Response

from bookmarks.models import Bookmark
from bookmarks.serializers import BookmarkSerializer


class BookmarkViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    serializer_class = BookmarkSerializer
    queryset = Bookmark.objects.all()
    permission_classes = [IsOwnerOrAdmin]

    def create(self, request, *args, **kwargs):
        return Response({'error': 'Failed to retrieve data from the provided URL.'}, status=200)
