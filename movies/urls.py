from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('', MoviesList.as_view(), name='movies_list_url'),

]