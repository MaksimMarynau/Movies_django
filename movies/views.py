from django.shortcuts import render
# from django.views.generic.base import View
from django.views.generic import ListView, DetailView
# Create your views here.

from .models import Movie

class MoviesView(ListView):
	""" List of movies """
	model = Movie
	queryset = Movie.objects.filter(draft=False)
	template_name = 'movies/movies.html'

 
class MovieDetailView(DetailView):
	"""Full description of the movie"""
	model = Movie
	slug_field = 'url'
	template_name = 'movies/movie_detail.html'