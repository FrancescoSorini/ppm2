from django.db import models
from django.utils.text import slugify
from users.models import CustomUser


#TODO: Migrazioni per creare le tabelle nel database

class Post(models.Model):
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='posts'
    )
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(CustomUser, related_name='liked_posts', blank=True)


    def __str__(self):
        return f"Post di {self.author.username} - {self.created_at.strftime('%d-%m-%Y %H:%M:%S')}"


    # Override del metodo save per generare uno titolo (dal contenuto) unico se non fornito
    def save(self, *args, **kwargs):
        if not self.title:
            base_slug = slugify(self.content[:30])
            unique_slug = base_slug
            counter = 1
            while Post.objects.filter(slug=unique_slug).exists():
                unique_slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = unique_slug

        super().save(*args, **kwargs)


class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Commento di {self.author.username} su Post {self.post.id} - {self.created_at.strftime('%d-%m-%Y %H:%M:%S')}"
