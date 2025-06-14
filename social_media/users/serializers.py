from rest_framework import serializers
from .models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):

    # Meta definisce le proprietà del modello da serializzare
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'bio', 'followers']
        read_only_fields = ['id', 'followers']


    # metodo per validare i dati in ingresso
    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user


    # aggiornamento custom per dati parziali
    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.bio = validated_data.get('bio', instance.bio)
        instance.save()
        return instance
