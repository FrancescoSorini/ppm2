from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from .permissions import IsAuthorOrReadOnly


class PostListCreateView(generics.ListCreateAPIView):
    """
    Elenca tutti i post o consente la creazione di un nuovo post.
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

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