from rest_framework.permissions import IsAuthenticated


class IsOwnerOrAdmin(IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        user = request.user
        owner = None
        try:
            owner = obj.owner
        except AttributeError as ae:
            owner = None
        finally:
            return user.is_staff or (owner and owner.pk == user.pk)
