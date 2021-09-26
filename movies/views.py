from django.db.models import Q
from django.shortcuts import render, redirect

# Create your views here.
from django.views import View
from django.views.generic import ListView, DetailView
from .models import Movie, Actor,Genre
from .forms import ReviewForm

class GenreYear():
    def get_genre(self):
        return Genre.objects.all()
    def get_year(self):
        return Movie.objects.filter(draft=False).values('year').distinct()

class MoviesList(GenreYear,ListView):
    model = Movie
    template_name = 'movies/movies.html'
    context_object_name = 'content'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        movies = self.model.objects.filter(draft=False)
        context['movies'] = movies
        return context

class MovieDetails(GenreYear, DetailView):
    model = Movie
    slug_field = 'url'
    template_name = 'movies/moviesingle.html'
    context_object_name = 'movie'

class ActorDetail(GenreYear,DetailView):
    model = Actor
    slug_field = 'url'
    template_name = 'movies/actor.html'
    context_object_name = 'actor'

class AddRewiew(View):
    def post(self, request, pk):
        form = ReviewForm(request.POST)
        movie = Movie.objects.get(id=pk)
        if form.is_valid():
            form = form.save(commit=False) #Зберігає усі поля із форми, але в Бд не пише
            if request.POST.get('parent',None):
                form.parent_id = int(request.POST.get('parent'))
            form.movie = movie
            form.save()

        return redirect(movie.get_absolute_url())

class FilteradMoviesList(GenreYear,ListView):
    template_name = 'movies/movies.html'
    context_object_name = 'content'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        movies = Movie.objects.filter(Q(draft=False) & Q(year__in=self.request.GET.getlist('year'))|Q(genres__in=self.request.GET.getlist('genre')))
        context['movies'] = movies
        return context

    # def get_queryset(self):
    #     queryset = Movie.objects.filter(Q(year__in=self.request.GET.getlist('year'))|Q(genres__in=self.request.GET.getlist('genre')))
    #     print(queryset)
    #     return queryset