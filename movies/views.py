from django.shortcuts import render, redirect
from django.views.generic.base import View
from django.views.generic import ListView, DetailView
# Create your views here.

from .models import Movie
from .forms import ReviewForm

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

class AddReview(View):
	""" Reviews """
	def post(self,request,pk):
		form = ReviewForm(request.POST)
		movie = Movie.objects.get(id=pk)
		if form.is_valid():
			form = form.save(commit=False)
			if request.POST.get("parent", None):
				form.parent_id = int(request.POST.get("parent"))
			form.movie = movie
			form.save() 
		return redirect(movie.get_absolute_url())