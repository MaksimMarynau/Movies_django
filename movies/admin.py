from django.contrib import admin

# Register your models here.
from .models import Category, Actor, Genre, Movie, MovieShots, RatingStar, Rating, Reviews

admin.site.register(Category)
admin.site.register(Actor)
admin.site.register(Genre)
admin.site.register(Movie)
admin.site.register(MovieShots)
admin.site.register(RatingStar)
admin.site.register(Rating)
admin.site.register(Reviews)