from rest_framework.routers import SimpleRouter

from bookmarks.views import BookmarkViewSet

bookmarks_router = SimpleRouter()
bookmarks_router.register("bookmarks", BookmarkViewSet, basename="bookmarks")

urlpatterns = []

urlpatterns += bookmarks_router.urls
