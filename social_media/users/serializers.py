from rest_framework import serializers
from .models import CustomUser
from posts.models import Post
from posts.serializers import CommentSerializer

class PostWithCommentsSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    likes_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'created_at', 'likes_count', 'comments']

    def get_likes_count(self, obj):
        return obj.likes.count()


class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    # visualizzazione dei campi followers e following tramite ID
    followers = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    following = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    # Visualizzazione dei propri post
    posts = PostWithCommentsSerializer(many=True, read_only=True)

    # Meta definisce le proprietà del modello da serializzare
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'password', 'bio', 'followers', 'following', 'posts']
        read_only_fields = ['id', 'followers', 'following', 'posts']

    # metodo per validare i dati in ingresso
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        if not password:
            raise serializers.ValidationError({"password": "La password è obbligatoria."})

        user = CustomUser.objects.create_user(password=password, **validated_data)
        return user

    # aggiornamento custom per dati parziali
    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        if password:
            instance.set_password(password)

        instance.username = validated_data.get('username', instance.username)
        instance.bio = validated_data.get('bio', instance.bio)
        instance.email = validated_data.get('email', instance.email)
        instance.save()
        return instance


