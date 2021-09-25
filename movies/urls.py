from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('', MoviesList.as_view(), name='movies_list_url'),
    path('review/<int:pk>/', AddRewiew.as_view(), name='add_review'),
    path('<slug:slug>/', MovieDetails.as_view(), name='movie_detail_url'),

]