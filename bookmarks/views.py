from django.db.models import Q
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, mixins, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from bookmarks.business.OPGInfoExtractor import OPGInfoExtractor
from bookmarks.models import Bookmark, LinkType, Collection
from bookmarks.permissions import IsOwnerOrAdmin
from bookmarks.serializers import BookmarkSerializer, BookmarkUrlSerializer, CollectionSerializer, \
    BookmarkCreateSerializer, CollectionCreateSerializer


class BookmarkViewSet(ModelViewSet):
    serializer_class = BookmarkSerializer
    queryset = Bookmark.objects.all()
    permission_classes = [IsOwnerOrAdmin]

    @extend_schema(responses={
        status.HTTP_201_CREATED: BookmarkCreateSerializer,
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

        user_same_url = self.get_queryset().filter(Q(owner=user.pk) & Q(link=info.get("url")))
        inst = None
        if user_same_url.exists():
            inst = user_same_url.first()

        bookmark_serializer = BookmarkCreateSerializer(instance=inst, data=model_data, partial=inst is not None)
        bookmark_serializer.is_valid(raise_exception=True)
        bookmark_serializer.save()
        headers = self.get_success_headers(bookmark_serializer.data)
        return Response(bookmark_serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset()
        if self.action == "list" and not user.is_staff:
            queryset = queryset.filter(owner=user)
        return queryset

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = [IsAuthenticated, ]
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action == "create":
            self.serializer_class = BookmarkUrlSerializer
        return super().get_serializer_class()


class CollectionViewSet(ModelViewSet):
    serializer_class = CollectionSerializer
    queryset = Collection.objects.all()
    permission_classes = [IsOwnerOrAdmin]

    def create(self, request, *args, **kwargs):
        data_with_user = {"owner": request.user.pk} | request.data
        serializer = self.get_serializer(data=data_with_user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset()
        if self.action == "list" and not user.is_staff:
            queryset = queryset.filter(owner=user)
        return queryset

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = [IsAuthenticated, ]
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action == "create":
            self.serializer_class = CollectionCreateSerializer
        return super().get_serializer_class()
