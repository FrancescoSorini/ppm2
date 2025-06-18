from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken, APIView
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import authenticate
from rest_framework import status

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


class CurrentUserAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'bio': user.bio,
            'is_staff': user.is_staff,

        })


# vista api per effettuare il login e restituire il token
@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def login_view(request):
    if request.method == 'GET':
        return Response({
            "message": "Usa POST con username e password per ottenere un token."
        })

    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)
    if user:
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.id,
            'username': user.username,
            'email': user.email,
            'bio': user.bio,
        })
    return Response({'error': 'Credenziali non valide'}, status=status.HTTP_401_UNAUTHORIZED)
