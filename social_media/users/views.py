from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken, APIView
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404

from .permissions import IsSelfOrAdmin, IsPublicOrAdmin
from .models import CustomUser
from .serializers import CustomUserSerializer
from notifications.models import Notification


class ListCreateUserAPIView(generics.ListCreateAPIView):
    """
    Elenca tutti gli utenti o consente la registrazione.
    """
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]


class UserRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    Permette all'utente di visualizzare, modificare o eliminare sé stesso.
    Oppure accesso admin per gestire tutti.
    """
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAuthenticated, IsPublicOrAdmin]



class CurrentUserAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = CustomUserSerializer(request.user)
        return Response(serializer.data)

    def patch(self, request):
        serializer = CustomUserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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


# Funzione per seguire utenti (tramite username)
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def follow_user(request, username):
    target_user = get_object_or_404(CustomUser, username=username)

    if request.user == target_user:
        return Response({"detail": "Non puoi seguire te stesso."}, status=400)
    if target_user in request.user.following.all():
        return Response({"detail": f"Stai già seguendo {target_user.username}."}, status=409)
    request.user.following.add(target_user)

    # Crea una notifica per l'utente seguito
    Notification.objects.create(
        sender=request.user,
        recipient=target_user,
        notification_type='follow',
        message=f"@{request.user.username} ha iniziato a seguirti."
    )
    return Response({"detail": f"Ora segui {target_user.username}."})


# Funzione per smettere di seguire utenti (tramite username)
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def unfollow_user(request, username):
    target_user = get_object_or_404(CustomUser, username=username)
    if request.user == target_user:
        return Response({"detail": "Non puoi smettere di seguire te stesso."}, status=400)
    if target_user not in request.user.following.all():
        return Response({"detail": f"Non stai seguendo {target_user.username}."}, status=400)
    request.user.following.remove(target_user)
    return Response({"detail": f"Hai smesso di seguire {target_user.username}."})


# Funzione per cercare utenti per username (usando query string)
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def search_users(request):
    query = request.query_params.get('q', '')
    users = CustomUser.objects.filter(username__icontains=query)
    serializer = CustomUserSerializer(users, many=True)
    return Response(serializer.data)
