from django.contrib import admin

# Register your models here.
from .models import Category, Actor, Genre, Movie, MovieShots, RatingStar, Rating, Reviews

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
	""" Categories """
	list_display = ('id', 'name', 'url')
	list_display_links = ('name',)

class ReviewInline(admin.StackedInline):
	""" Reviews on movie card """
	model = Reviews
	extra = 1
	readonly_fields = ('name','email')

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
	""" Movies """
	list_display = ('title','category','url','draft')
	list_filter = ('category','year')
	search_fields = ('title','category__name')
	inlines = [ReviewInline]
	save_on_top = True
	save_as = True
	list_editable = ('draft',)
	# fields = (('actors','directors','genres'),)
	fieldsets = (
		(None, {
			'fields':(('title','tagline'),)
		}),
		(None, {
			'fields':('description','poster')
		}),
		(None, {
			'fields':(('year','world_premiere','country'),)
		}),
		('Actors', {
			'classes': ('collapse',),
			'fields':(('actors','directors','genres','category'),)
		}),
		(None, {
			'fields':(('budget','fees_in_usa','fees_in_world'),)
		}),
		('Options', {
			'fields':(('url','draft'),)
		}),
	)

@admin.register(Reviews)
class ReviewsAdmin(admin.ModelAdmin):
	""" Reviews """
	list_display = ('name','text','email','parent','movie','id')
	readonly_fields = ('name','email')

@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
	""" Actors """
	list_display = ('name','age')

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
	""" Genres """
	list_display = ('name','url')

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
	""" Ratings """
	list_display = ('ip','movie','star')

@admin.register(MovieShots)
class MovieShotsAdmin(admin.ModelAdmin):
	""" Shots from movie """
	list_display = ('title','movie')

admin.site.register(RatingStar)

