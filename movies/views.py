from django.shortcuts import render, redirect

# Create your views here.
from django.views import View
from django.views.generic import ListView, DetailView
from .models import Movie
from .forms import ReviewForm

class MoviesList(ListView):
    model = Movie
    template_name = 'movies/movies.html'
    context_object_name = 'content'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        movies = self.model.objects.filter(draft=False)

        context['movies'] = movies
        return context

class MovieDetails(DetailView):
    model = Movie
    slug_field = 'url'
    template_name = 'movies/moviesingle.html'
    context_object_name = 'movie'


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