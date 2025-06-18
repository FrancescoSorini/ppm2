from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth.hashers import make_password


class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    # Meta definisce le proprietà del modello da serializzare
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'password', 'bio', 'followers', 'following']
        read_only_fields = ['id', 'followers', 'following']

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
        instance.save()
        return instance
