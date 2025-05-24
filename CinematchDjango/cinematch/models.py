from django.db import models
from django.contrib.auth.models import User

class FavoriteMovie(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorite_movies')
    title = models.CharField(max_length=255)
    poster_url = models.URLField()

    def __str__(self):
        return f"{self.user.username} - {self.title}" 