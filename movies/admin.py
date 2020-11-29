from django.contrib import admin
from django.utils.safestring import mark_safe
from django import forms
# Register your models here.
from .models import Category, Actor, Genre, Movie, MovieShots, RatingStar, Rating, Reviews


from ckeditor_uploader.widgets import CKEditorUploadingWidget


class MovieAdminForm(forms.ModelForm):
    description = forms.CharField( label='Description', widget=CKEditorUploadingWidget())
    
    class Meta:
        model = Movie
        fields = '__all__'


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

class MovieShotsInline(admin.StackedInline):
	""" Shots from movie """
	model = MovieShots
	extra = 1
	readonly_fields = ('get_image',)

	def get_image(self,obj):
		return mark_safe(f'<img src={obj.image.url} width="100" height="auto"')

	get_image.short_description = 'Shots'

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
	""" Movies """
	list_display = ('title','category','url','draft')
	list_filter = ('category','year')
	search_fields = ('title','category__name')
	inlines = [MovieShotsInline, ReviewInline]
	save_on_top = True
	save_as = True
	list_editable = ('draft',)
	# fields = (('actors','directors','genres'),)
	form = MovieAdminForm
	readonly_fields = ('get_poster',)
	fieldsets = (
		(None, {
			'fields':(('title','tagline'),)
		}),
		(None, {
			'fields':('description',('poster','get_poster'),)
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

	def get_poster(self,obj):
		return mark_safe(f'<img src={obj.poster.url} width="100" height="auto"')

	get_poster.short_description = 'Poster'

@admin.register(Reviews)
class ReviewsAdmin(admin.ModelAdmin):
	""" Reviews """
	list_display = ('name','text','email','parent','movie','id')
	readonly_fields = ('name','email')

@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
	""" Actors and directos """
	list_display = ('name','age','get_image')
	readonly_fields = ('get_image',)

	def get_image(self,obj):
		return mark_safe(f'<img src={obj.image.url} width="50" height="60"')

	get_image.short_description = 'Image'

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
	list_display = ('title','movie','get_image')
	readonly_fields = ('get_image',)

	def get_image(self,obj):
		return mark_safe(f'<img src={obj.image.url} width="80" height="auto"')

	get_image.short_description = 'Shots'


admin.site.register(RatingStar)

admin.site.site_title = "Django movies"
admin.site.site_header = "Django movies"

