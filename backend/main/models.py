"""
Django models for the main app.
"""
from django.db import models
from django.contrib.auth.models import User


class Genre(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Studio(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class ListStatus(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name


class Anime(models.Model):
    title = models.CharField(max_length=200, null=False)
    type = models.CharField(max_length=20, blank=True, null=True)
    synopsis = models.TextField(blank=True, null=True)
    total_episodes = models.IntegerField(blank=True, null=True)
    status = models.CharField(max_length=20, blank=True, null=True)
    aired_from = models.DateField(blank=True, null=True)
    aired_to = models.DateField(blank=True, null=True)
    image_url = models.TextField(blank=True, null=True)
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    rating_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    genres = models.ManyToManyField(Genre, through='AnimeGenre')
    studios = models.ManyToManyField(Studio, through='AnimeStudio')

    def __str__(self):
        return self.title

    def calculate_average_rating(self):
        return self.average_rating / self.rating_count if self.rating_count > 0 else 0.00


class AnimeGenre(models.Model):
    anime = models.ForeignKey(Anime, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('anime', 'genre')


class AnimeStudio(models.Model):
    anime = models.ForeignKey(Anime, on_delete=models.CASCADE)
    studio = models.ForeignKey(Studio, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('anime', 'studio')


class UserAnimeList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    anime = models.ForeignKey(Anime, on_delete=models.CASCADE)
    status = models.ForeignKey(ListStatus, on_delete=models.CASCADE)
    score = models.SmallIntegerField(blank=True, null=True)
    episodes_watched = models.IntegerField(default=0)
    start_date = models.DateField(blank=True, null=True)
    finish_date = models.DateField(blank=True, null=True)
    priority = models.SmallIntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'anime')


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    anime = models.ForeignKey(Anime, on_delete=models.CASCADE)
    score = models.SmallIntegerField()
    review_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Tag(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class ListTag(models.Model):
    user_list = models.ForeignKey(UserAnimeList, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user_list', 'tag')