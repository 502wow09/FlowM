from django.contrib import admin

# Register your models here.
from movies.models import Movie, Configuration, Genre

admin.site.register(Movie)
admin.site.register(Configuration)
admin.site.register(Genre)