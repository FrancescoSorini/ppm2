from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from .permissions import IsAuthorOrReadOnly
from notifications.models import Notification
from notifications.utils import notify_mentions


# TODO: Rivedere la ricerca dei commenti, usare ID al posto di slug


class PostListCreateView(generics.ListCreateAPIView):
    """
    Elenca tutti i post o consente la creazione di un nuovo post.
    """
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        post = serializer.save(author=self.request.user)

        notify_mentions(post.content, self.request.user, post_id=post.id)


class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Visualizza, modifica o elimina un post specifico.
    Solo l'autore del post può modificarlo o eliminarlo.
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthorOrReadOnly]

    # Override per ottenere post specifico tramite user-friendly slug
    def get_object(self):
        post_id = self.kwargs.get('pk')
        post = get_object_or_404(Post, pk=post_id)
        self.check_object_permissions(self.request, post)
        return post


# Mettere e togliere like ai post
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def toggle_like_post(request, post_id):
    """
    Aggiunge o rimuove un like a un post.
    """
    post = get_object_or_404(Post, pk=post_id)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
        return Response({'message': 'Hai tolto il mi piace.'}, status=status.HTTP_200_OK)
    else:
        post.likes.add(request.user)

        # Notifica l'autore del post che qualcuno ha messo mi piace
        if request.user not in post.likes.all():
            post.likes.add(request.user)
            if request.user != post.author:
                Notification.objects.create(
                    sender=request.user,
                    recipient=post.author,
                    notification_type='like',
                    post_id=post.id,
                    message=f"@{request.user.username} ha messo mi piace al tuo post: {post.title}"
                )
        return Response({'message': 'Hai messo mi piace!'}, status=status.HTTP_200_OK)


# Commentare un post specifico
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def create_comment(request, post_id):
    """
    Crea un commento su un post specifico.
    """
    post = get_object_or_404(Post, pk=post_id)
    serializer = CommentSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save(author=request.user, post=post)

        # Notifica l'autore del post che qualcuno ha commentato
        if request.user != post.author:
            Notification.objects.create(
                sender=request.user,
                recipient=post.author,
                notification_type='comment',
                post_id=post.id,
                message=f"@{request.user.username} ha commentato il tuo post: {post.title}"
            )

        # Notifica per menzioni nei commenti
        notify_mentions(request.data.get("content", ""), request.user, post_id=post.id)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Elencare i commenti di un post specifico
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticatedOrReadOnly])
def list_comments(request, post_id):
    """
    Elenca tutti i commenti di un post specifico.
    """
    post = get_object_or_404(Post, pk=post_id)
    comments = post.comments.all().order_by('-created_at')
    serializer = CommentSerializer(comments, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


# Eliminare un commento specifico
@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticated])
def delete_comment(request, comment_id):
    """
    Elimina un commento se l'utente è autore o admin.
    """
    comment = get_object_or_404(Comment, id=comment_id)

    if request.user != comment.author and not request.user.is_staff:
        return Response({'error': 'Non hai i permessi per eliminare questo commento.'},
                        status=status.HTTP_403_FORBIDDEN)

    comment.delete()
    return Response({'message': 'Commento eliminato con successo.'}, status=status.HTTP_204_NO_CONTENT)
