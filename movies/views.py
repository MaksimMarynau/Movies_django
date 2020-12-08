from django.shortcuts import render, redirect
from django.views.generic.base import View
from django.views.generic import ListView, DetailView
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.conf import settings
# Create your views here.

from .models import Movie, Category, Actor, Genre, Rating, Reviews
from .forms import ReviewForm, RatingForm

class GenreYear:
	""" Genre and year released """
	def get_genres(self):
		return Genre.objects.all().order_by("name")

	def get_years(self):
		return Movie.objects.filter(draft=False).order_by("year").values("year")


class MoviesView(GenreYear, ListView):
	""" List of movies """
	model = Movie
	queryset = Movie.objects.filter(draft=False)
	# template_name = 'movies/movie_list.html'
	paginate_by = 3


class MovieDetailView(GenreYear, DetailView):
	"""Full description of the movie"""
	model = Movie
	slug_field = 'url'
	# template_name = 'movies/movie_detail.html'

	def get_user_stars(self, ip, movie_id):
	    if Rating.objects.filter(ip=ip, movie_id=movie_id).exists():
	    	stars = Rating.objects.get(ip=ip, movie_id=movie_id).star
	    else:
	    	stars = None
	    return stars

	def get(self, request, *args, **kwargs):
		ip = AddStarRating.get_client_ip(self, self.request)
		movie_id = Movie.objects.get(url=kwargs['slug']).id
		stars = self.get_user_stars(ip, movie_id)
		self.object = self.get_object()
		context = self.get_context_data(object=self.request)
		if stars:
			context['stars'] = str(stars)
		return self.render_to_response(context)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["star_form"] = RatingForm()
		context["form"] = ReviewForm()
		return context


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


class ActorView(GenreYear, DetailView):
	""" Information about actors """
	model = Actor
	template_name = "movies/actor.html"
	slug_field = "name"


class FilterMoviesView(GenreYear, ListView):
	""" Movies filter """
	paginate_by = 2

	def get_queryset(self):
		queryset = Movie.objects.filter(
			Q(year__in = self.request.GET.getlist("year")) |
			Q(genres__in = self.request.GET.getlist("genre"))
		).distinct()
		return queryset

	def get_context_data(self, *args, **kwargs):
		context = super().get_context_data(*args, **kwargs)
		context["year"] = ''.join([f"year={x}&" for x in self.request.GET.getlist("year")])
		context["genre"] = ''.join([f"genre={x}&" for x in self.request.GET.getlist("genre")])
		return context

class JsonFilterMoviesView(ListView):
	""" Movies filter in json """
	def get_queryset(self):
		queryset = Movie.objects.filter(
			Q(year__in = self.request.GET.getlist("year")) |
			Q(genres__in = self.request.GET.getlist("genre"))
		).distinct().values('title','tagline','url','poster')
		return queryset

	def get(self, request, *args, **kwargs):
		queryset = list(self.get_queryset())
		return JsonResponse({'movies':queryset}, safe=False)


class AddStarRating(View):
    """Add rating to movie"""
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def post(self, request):
        form = RatingForm(request.POST)
        if form.is_valid():
            Rating.objects.update_or_create(
                ip=self.get_client_ip(request),
                movie_id=int(request.POST.get("movie")),
                defaults={'star_id': int(request.POST.get("star"))}
            )
            return HttpResponse(status=201)
        else:
            return HttpResponse(status=400)

class Search(GenreYear, ListView):
	"""Search movie"""

	paginate_by = 3

	def get_queryset(self):
		return Movie.objects.filter(title__icontains=self.request.GET.get("q"))

	def get_context_data(self,*args,**kwargs):
	    context = super().get_context_data(*args,**kwargs)
	    context["q"] = f'{self.request.GET.get("q")}&'
	    return context
