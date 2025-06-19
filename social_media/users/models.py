from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    username = models.CharField(
        max_length=150,
        unique=True,
    )
    bio = models.TextField(blank=True, null=True)
    followers = models.ManyToManyField(
        'self',
        symmetrical=False,  # consente di seguire senza che l'utente debba ricambiare il follow
        related_name='following',  # per vedere chi segue l'utente
        blank=True,
    )

    def __str__(self):
        return self.username
