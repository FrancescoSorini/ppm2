from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import CustomUser
from .serializers import CustomUserSerializer


class ListCreateUserView(generics.ListCreateAPIView):
    """
    Vista per elencare e creare nuovi utenti.
    Supporta la visualizzazione di tutti gli utenti
    """
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()  # Salva l'utente con i dati validati


class RetrieveUpdateDestroyUserView(generics.RetrieveUpdateDestroyAPIView):
    """
    Vista per recuperare, aggiornare o eliminare un utente specifico.
    Supporta la visualizzazione, l'aggiornamento e l'eliminazione di un utente specifico
    """
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def perform_update(self, serializer):
        serializer.save()  # Salva le modifiche all'utente con i dati validati


    def perform_destroy(self, instance):
        instance.delete()  # Elimina l'utente specificato

