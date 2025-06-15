from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    username = models.CharField(
        max_length=150,
        unique=True,
        #error_messages={'unique': "A user with that username already exists."}
    )
    bio = models.TextField(blank=True, null=True)
    followers = models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name='following',
        blank=True,
    )

    def __str__(self):
        return self.username
