from django.db import transaction
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, mixins, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from bookmarks.business.OPGInfoExtractor import OPGInfoExtractor
from bookmarks.models import Bookmark, LinkType
from bookmarks.permissions import IsOwnerOrAdmin
from bookmarks.serializers import BookmarkSerializer, BookmarkUrlSerializer


class BookmarkViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    serializer_class = BookmarkUrlSerializer
    queryset = Bookmark.objects.all()
    permission_classes = [IsOwnerOrAdmin]

    @extend_schema(responses={
        status.HTTP_201_CREATED: BookmarkSerializer,
    })
    def create(self, request, *args, **kwargs):
        user = request.user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        ogp_extractor = OPGInfoExtractor(request.data.get("target_url"))
        ogp_extractor.extract()
        info = ogp_extractor.info()

        model_data = {
            "owner": user.pk,
            "title": info.get("title"),
            "description": info.get("description"),
            "link": info.get("url"),
            "image": info.get("image", "")
        }

        link_type = LinkType.objects.filter(pk=info.get("type"))
        if link_type.exists():
            model_data |= {
                "link_type": link_type.first().pk
            }

        bookmark_serializer = BookmarkSerializer(data=model_data)
        bookmark_serializer.is_valid(raise_exception=True)
        bookmark_serializer.save()
        headers = self.get_success_headers(bookmark_serializer.data)
        return Response(bookmark_serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = [IsAuthenticated, ]
        return super().get_permissions()
