from django.urls import path, include
from .views import (
    ListCreateUserAPIView,
    UserRetrieveUpdateDestroyAPIView,
    CustomAuthToken,
    login_view,
    CurrentUserAPIView,
    follow_user,
    unfollow_user,
    search_users
)

urlpatterns = [
    # Registrazione nuovi utenti (POST) | Lista utenti (GET)
    path("users/", ListCreateUserAPIView.as_view(), name="create-list-users"),

    # Recupera, aggiorna o cancella un utente (solo admin o self)
    path('users/<int:pk>/', UserRetrieveUpdateDestroyAPIView.as_view(), name='get-update-delete-user'),

    # Recupera l'utente corrente
    path('users/me', CurrentUserAPIView.as_view(), name='current-user'),

    # Login tramite username e password
    path('login/', login_view, name='users-login'),

    # Login tramite token
    path('token-login/', CustomAuthToken.as_view(), name='users-login'),

    # Autenticazione tramite token
    path('api-auth/', include('rest_framework.urls')),

    # Segui un utente
    path('users/<int:user_id>/follow/', follow_user, name='follow-user'),

    # Smetti di seguire un utente
    path("users/<int:user_id>/unfollow/", unfollow_user, name="unfollow-user"),

    #cerca utente per username
    path('users/search/', search_users, name='search-users'),
]

