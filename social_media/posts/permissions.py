from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Permesso che consente modifiche solo all'autore del post o commento.
    Gli altri utenti possono solo leggere.
    """

    def has_object_permission(self, request, view, obj):
        # Le richieste GET, HEAD, OPTIONS sono sempre permesse
        if request.method in permissions.SAFE_METHODS:
            return True

        # Permesso solo se l'utente è l'autore dell'oggetto
        return obj.author == request.user


class IsAdminUser(permissions.BasePermission):
    """
    Solo gli admin possono eseguire qualsiasi azione.
    Gli altri utenti devono essere autenticati ma possono solo leggere.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_staff
