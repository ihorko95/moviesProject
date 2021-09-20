from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView
from .models import Movie


class MoviesList(ListView):
    model = Movie
    template_name = 'movies.html'
    context_object_name = 'content'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        movies = self.model.objects.all()
        context['movies'] = movies
        return context
