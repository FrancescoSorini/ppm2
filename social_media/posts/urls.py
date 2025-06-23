from django.urls import path
from .views import (
    PostListCreateView,
    PostDetailView,
    toggle_like_post,
    create_comment,
    list_comments,
    delete_comment
)

urlpatterns = [
    #  Lista e creazione post
    path('posts', PostListCreateView.as_view(), name='posts-list-create'),

    #  Dettaglio, modifica ed eliminazione post tramite ID
    path('<int:pk>', PostDetailView.as_view(), name='post-detail'),

    #  Like/unlike tramite ID
    path('<int:post_id>/like', toggle_like_post, name='post-toggle-like'),

    #  Lista commenti tramite ID
    path('<int:post_id>/comments', list_comments, name='post-comments-list'),

    #  Creazione commento tramite ID
    path('<int:post_id>/comments/add', create_comment, name='post-add-comment'),

    #  Eliminazione commento tramite ID
    path('comments/<int:comment_id>/delete', delete_comment, name='comment-delete'),

]


