from django.contrib import admin

# Register your models here.
from movies.models import Movie, Configuration, Genre, Movie_Genre, Keyword, Movie_Keyword

admin.site.register(Movie)
admin.site.register(Configuration)
admin.site.register(Genre)
admin.site.register(Movie_Genre)
admin.site.register(Keyword)
admin.site.register(Movie_Keyword)