from django.urls import path
from .views import (
    PostListCreateView,
    PostDetailView,
    toggle_like_post,
    create_comment,
    list_comments
)

urlpatterns = [
    #  Lista e creazione post
    path('posts/', PostListCreateView.as_view(), name='posts-list-create'),

    #  Dettaglio, modifica ed eliminazione post tramite slug
    path('posts/<slug:slug>/', PostDetailView.as_view(), name='post-detail'),

    #  Like/unlike tramite slug
    path('posts/<slug:slug>/like/', toggle_like_post, name='post-toggle-like'),

    #  Lista commenti tramite slug
    path('posts/<slug:slug>/comments/', list_comments, name='post-comments-list'),

    #  Creazione commento tramite slug
    path('posts/<slug:slug>/comments/add/', create_comment, name='post-add-comment'),
]


