from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Permesso customizzato che consente agli utenti di modificare solo gli oggetti che possiedono.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.owner == request.user


class IsAdminUser(permissions.BasePermission):
    """
    Solo gli admin possono modificare, altri solo in lettura.
    """

    def has_permission(self, request, view):
        # Controlla se l'utente è autenticato e se è un admin
        return request.user and request.user.is_authenticated and request.user.is_staff


class IsSelfOrAdmin(permissions.BasePermission):
    """
    Permette l'accesso solo se l'utente è sé stesso o è admin.
    """

    def has_object_permission(self, request, view, obj):
        return request.user == obj or request.user.is_staff
