from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken

from .permissions import IsSelfOrAdmin
from .models import CustomUser
from .serializers import CustomUserSerializer


class ListCreateUserAPIView(generics.ListCreateAPIView):
    """
    Elenca tutti gli utenti (solo admin) o consente la registrazione.
    """
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]


class UserRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    Permette all'utente di visualizzare, modificare o eliminare sé stesso.
    Oppure accesso admin per gestire tutti.
    """
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAuthenticated, IsSelfOrAdmin]


class CustomAuthToken(ObtainAuthToken):
    """
    Restituisce token + info utente dopo login.
    """
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        user = token.user
        return Response({
            'token': token.key,
            'user_id': user.id,
            'username': user.username,
            'email': user.email
        })