from django.urls import path
from .views import (
    ListCreateUserAPIView,
    UserRetrieveUpdateDestroyAPIView,
    CustomAuthToken,
)

urlpatterns = [
    # Registrazione nuovi utenti (POST) | Lista utenti (GET solo admin)
    path("users/", ListCreateUserAPIView.as_view(), name="create-list-users"),

    # Recupera, aggiorna o cancella un utente (solo admin o self)
    path('users/<int:pk>/', UserRetrieveUpdateDestroyAPIView.as_view(), name='get-update-delete-user'),

    # Login tramite token
    path('login/', CustomAuthToken.as_view(), name='users-login'),
]

