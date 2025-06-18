from django.urls import path, include
from .views import (
    ListCreateUserAPIView,
    UserRetrieveUpdateDestroyAPIView,
    CustomAuthToken,
    login_view,
    CurrentUserAPIView
)

urlpatterns = [
    # Registrazione nuovi utenti (POST) | Lista utenti (GET solo admin)
    path("users/", ListCreateUserAPIView.as_view(), name="create-list-users"),

    # Recupera, aggiorna o cancella un utente (solo admin o self)
    path('users/<int:pk>/', UserRetrieveUpdateDestroyAPIView.as_view(), name='get-update-delete-user'),

    # Recupera l'utente corrente
    path('users/me', CurrentUserAPIView.as_view(), name='current-user'),

    # Login tramite username e password
    path('login/', login_view, name='users-login'),

    # Login tramite token
    path('token-login/', CustomAuthToken.as_view(), name='users-login'),

    path('api-auth/', include('rest_framework.urls')),
]

