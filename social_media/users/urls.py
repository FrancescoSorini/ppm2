from django.urls import path
from .views import (
    ListCreateUserAPIView,
    UserRetrieveUpdateDestroyAPIView,
    CustomAuthToken,
    login_view
)

urlpatterns = [
    # Registrazione nuovi utenti (POST) | Lista utenti (GET solo admin)
    path("users/", ListCreateUserAPIView.as_view(), name="create-list-users"),

    # Recupera, aggiorna o cancella un utente (solo admin o self)
    path('users/<int:pk>/', UserRetrieveUpdateDestroyAPIView.as_view(), name='get-update-delete-user'),

    # Login tramite username e password
    path('login/', login_view, name='users-login'),

    # Login tramite token
    path('token-login/', CustomAuthToken.as_view(), name='users-login'),
]

