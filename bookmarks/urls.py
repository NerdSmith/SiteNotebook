from rest_framework.routers import SimpleRouter

from bookmarks.views import BookmarkViewSet, CollectionViewSet

bookmarks_router = SimpleRouter()
bookmarks_router.register("bookmarks", BookmarkViewSet, basename="bookmarks")
bookmarks_router.register("collections", CollectionViewSet, basename="collections")

urlpatterns = []

urlpatterns += bookmarks_router.urls
