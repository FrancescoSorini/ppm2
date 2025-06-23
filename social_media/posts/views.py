from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from .permissions import IsAuthorOrReadOnly


# TODO: Rivedere la ricerca dei commenti, usare ID al posto di slug


class PostListCreateView(generics.ListCreateAPIView):
    """
    Elenca tutti i post o consente la creazione di un nuovo post.
    """
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


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
        slug = self.kwargs.get('slug')
        post = get_object_or_404(Post, slug=slug)
        self.check_object_permissions(self.request, post)
        return post


# Mettere e togliere like ai post
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def toggle_like_post(request, slug):
    """
    Aggiunge o rimuove un like a un post.
    """
    post = get_object_or_404(Post, slug=slug)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
        return Response({'message': 'Hai tolto il mi piace.'}, status=status.HTTP_200_OK)
    else:
        post.likes.add(request.user)
        return Response({'message': 'Hai messo mi piace!'}, status=status.HTTP_200_OK)


# Commentare un post specifico
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def create_comment(request, slug):
    """
    Crea un commento su un post specifico.
    """
    post = get_object_or_404(Post, slug=slug)
    serializer = CommentSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save(author=request.user, post=post)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Elencare i commenti di un post specifico
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticatedOrReadOnly])
def list_comments(request, slug):
    """
    Elenca tutti i commenti di un post specifico.
    """
    post = get_object_or_404(Post, slug=slug)
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
