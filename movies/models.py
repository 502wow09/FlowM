from django.db import models

# Create your models here.
class Movie(models.Model):
    id = models.IntegerField(default=0, primary_key=True, blank=True)
    title = models.CharField(max_length=100)
    original_title = models.CharField(max_length=100)
    popularity = models.FloatField(default=0)
    vote_average = models.FloatField(default=0)
    release_date = models.CharField(max_length=10)
    overview = models.TextField()
    backdrop_path = models.TextField()
    poster_path = models.TextField()
    video_path = models.TextField()

class Similar(models.Model):
    search_id = models.ForeignKey(Movie, on_delete=models.CASCADE)
    recommand_id = models.IntegerField(default=0)

class Configuration(models.Model):
    thumbnail_size = models.CharField(max_length=5) #'w185'
    poster_size = models.CharField(max_length=5) #'w342', 'original'
    backdrop_size = models.CharField(max_length=10) #'original'

class Genre(models.Model):
    id = models.IntegerField(default=0, primary_key=True, blank=True)
    name = models.CharField(max_length=10)

class Movie_Genre(models.Model):
    movie_id = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='movie_genre')
    genre_id = models.ForeignKey(Genre, on_delete=models.CASCADE, related_name='movie_genre')

class User(models.Model):
    id = models.IntegerField(default=0, primary_key=True)
    nickname = models.CharField(max_length=10)

class Keyword(models.Model):
    id = models.IntegerField(default=0, primary_key=True)
    name = models.CharField(max_length=20)

class Movie_Keyword(models.Model):
    movie_id = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='movie_keyword')
    keyword_id = models.ForeignKey(Keyword, on_delete=models.CASCADE, related_name='movie_keyword')

class Director(models.Model):
    id = models.IntegerField(default=0, primary_key=True)
    name = models.CharField(max_length=50)
    original_name = models.CharField(max_length=50)

class Movie_Director(models.Model):
    movie_id = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='movie_director')
    director_id = models.ForeignKey(Director, on_delete=models.CASCADE, related_name='movie_director')

class Actor(models.Model):
    id = models.IntegerField(default=0, primary_key=True)
    name = models.CharField(max_length=50)
    original_name = models.CharField(max_length=50)

class Movie_Actor(models.Model):
    movie_id = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='movie_actor')
    actor_id = models.ForeignKey(Actor, on_delete=models.CASCADE, related_name='movie_actor')    


class Movie_user(models.Model):
    movie_id = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='user_movie', blank=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_movie', blank=True)

class User_Keyword(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_keyword')
    keyword_id = models.ForeignKey(Keyword, on_delete=models.CASCADE, related_name='user_keyword')

class Comment(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField('date created')
    updated_at = models.DateTimeField('date updated')

