from django.contrib import admin

# Register your models here.
from movies.models import Movie, Configuration, Genre, Movie_Genre, Keyword, Movie_Keyword, Movie_Director, Movie_Actor, Similar, Likes, Querylist

admin.site.register(Movie)
admin.site.register(Configuration)
admin.site.register(Genre)
admin.site.register(Movie_Genre)
admin.site.register(Keyword)
admin.site.register(Movie_Keyword)
admin.site.register(Movie_Director)
admin.site.register(Movie_Actor)
admin.site.register(Similar)
admin.site.register(Likes)
admin.site.register(Querylist)
