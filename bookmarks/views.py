from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from bookmarks.models import Bookmark
from bookmarks.permissions import IsOwnerOrAdmin
from bookmarks.serializers import BookmarkSerializer


class BookmarkViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    serializer_class = BookmarkSerializer
    queryset = Bookmark.objects.all()
    permission_classes = [IsOwnerOrAdmin]

    def create(self, request, *args, **kwargs):
        return Response({'error': 'Failed to retrieve data from the provided URL.'}, status=200)

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = [IsAuthenticated, ]
        return super().get_permissions()
