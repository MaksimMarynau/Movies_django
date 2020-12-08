from django import template
from movies.models import Category, Movie


register = template.Library()

@register.simple_tag()
def get_category():
	""" Show all categories """
	return Category.objects.all()

@register.inclusion_tag("movies/tags/last_movies.html")
def get_last_movie(count=5):
	"""Show last movie"""
	movies = Movie.objects.order_by('-id')[:count]
	return {"last_movies": movies}