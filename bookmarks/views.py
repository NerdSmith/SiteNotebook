from django.db.models import Q, QuerySet
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from bookmarks.business.OGPInfoExtractor import OGPInfoExtractor
from bookmarks.models import Bookmark, LinkType, Collection
from bookmarks.permissions import IsOwnerOrAdmin
from bookmarks.serializers import BookmarkSerializer, BookmarkUrlSerializer, CollectionSerializer, \
    BookmarkCreateSerializer, CollectionCreateSerializer, BookmarkToCollectionSerializer


@extend_schema_view(
    list=extend_schema(description='Lists all bookmarks of current user. (All for Admin)'),
    create=extend_schema(description='Creates a new bookmark by url. If the user has the same url, then the bookmark '
                                     'is updated.'),
    retrieve=extend_schema(description='Gets bookmark by id.'),
    update=extend_schema(description='Updates bookmark by id.'),
    partial_update=extend_schema(description='Updates bookmark by id. (Partial)'),
    destroy=extend_schema(description='Deletes bookmark by id.'),
)
class BookmarkViewSet(ModelViewSet):
    serializer_class = BookmarkSerializer
    queryset = Bookmark.objects.all()
    permission_classes = [IsOwnerOrAdmin]

    @extend_schema(
        responses={
            status.HTTP_201_CREATED: BookmarkCreateSerializer,
        })
    def create(self, request, *args, **kwargs):
        user = request.user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        ogp_extractor: OGPInfoExtractor = OGPInfoExtractor(request.data.get("target_url"))
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

    def get_queryset(self) -> QuerySet["Bookmark"]:
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


@extend_schema_view(
    list=extend_schema(description='Lists all collections of current user. (All for Admin)'),
    create=extend_schema(description='Creates a new collection by title and description.'),
    retrieve=extend_schema(description='Gets collection by id.'),
    update=extend_schema(description='Updates collection by id.'),
    partial_update=extend_schema(description='Updates collection by id. (Partial)'),
    destroy=extend_schema(description='Deletes collection by id.'),
)
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
        elif self.action in ["add_bookmarks", "remove_bookmarks"]:
            self.serializer_class = BookmarkToCollectionSerializer
        return super().get_serializer_class()

    @extend_schema(
        description="Adds bookmarks to collection by id.",
        responses={
            status.HTTP_200_OK: CollectionSerializer,
        })
    @action(["patch"], detail=True)
    def add_bookmarks(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        collection = self.get_object()
        collection.add_bookmarks(serializer.data.get('bookmarks'))

        serializer_data = CollectionSerializer(instance=collection).data
        headers = self.get_success_headers(serializer.data)
        return Response(serializer_data, status=status.HTTP_200_OK, headers=headers)

    @extend_schema(
        description="Removes bookmarks from collection by id.",
        responses={
            status.HTTP_200_OK: CollectionSerializer,
        })
    @action(["patch"], detail=True)
    def remove_bookmarks(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        collection = self.get_object()
        collection.remove_bookmarks(serializer.data.get('bookmarks'))

        serializer_data = CollectionSerializer(instance=collection).data
        headers = self.get_success_headers(serializer.data)
        return Response(serializer_data, status=status.HTTP_204_NO_CONTENT, headers=headers)
