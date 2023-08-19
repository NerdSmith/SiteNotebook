from django.db import models
from django.utils.translation import gettext_lazy as _

from user_auth.models import User


class LinkType(models.Model):
    type = models.CharField(_('Link type'), max_length=20, primary_key=True)


class Bookmark(models.Model):
    owner = models.ForeignKey(User, related_name="user_bookmarks", on_delete=models.CASCADE, null=False, blank=False)
    title = models.CharField(_('Title'), max_length=100)
    description = models.CharField(_('Description'), max_length=500)
    link = models.URLField(_("Link"), max_length=2048)
    link_type = models.ForeignKey(LinkType, on_delete=models.SET_DEFAULT, default="website", null=False, blank=False)
    image = models.URLField(_("Image"), max_length=2048, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Bookmark -> {self.link} -> {self.title} CRT: {self.created_at} MOD:{self.modified_at}"

    class Meta:
        unique_together = [("owner", "link")]


class Collection(models.Model):
    owner = models.ForeignKey(User, related_name="user_collections", on_delete=models.CASCADE, null=False, blank=False)
    title = models.CharField(_('Title'), max_length=100)
    description = models.CharField(_('Description'), max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    bookmarks = models.ManyToManyField(Bookmark, related_name="bookmark_collections")

    def add_bookmarks(self, bookmarks):
        self.bookmarks.add(*bookmarks)

    def add_bookmark(self, bookmark):
        self.add_bookmarks([bookmark])

