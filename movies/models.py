from django.db import models
from datetime import date

# Create your models here.
from django.urls import reverse


class Category(models.Model):
    name = models.CharField('Category', max_length=40)
    description = models.TextField('Description', max_length=150, blank=True)
    url = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Actor(models.Model):
    name = models.CharField(max_length=50)
    age = models.PositiveSmallIntegerField(default=0)
    description = models.TextField('Description', max_length=150, blank=True)
    image = models.ImageField('Image', upload_to='actors/')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Actors and Directors'
        verbose_name_plural = 'Actors and Directors'


class Genre(models.Model):
    name = models.CharField('Category', max_length=40)
    description = models.TextField('Description', max_length=150, blank=True)
    url = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Movie(models.Model):
    title = models.CharField(max_length=100)
    tagline = models.CharField(max_length=500, default='')
    description = models.TextField(max_length=150, blank=True)
    poster = models.ImageField('Logo', upload_to='movies/')
    year = models.PositiveSmallIntegerField(default=int(str(date.today())[:4]))
    country = models.CharField(max_length=30, default='')
    directors = models.ManyToManyField(Actor, verbose_name='director', related_name='film_director')
    actors = models.ManyToManyField(Actor, verbose_name='actors', related_name='film_actor')
    genres = models.ManyToManyField(Genre)
    world_premier = models.DateField('Premier', default=date.today)
    budget = models.PositiveSmallIntegerField(default=0, help_text='Set in $')
    fees_in_usa = models.PositiveSmallIntegerField(default=0, help_text='Set in $')
    fees_in_world = models.PositiveSmallIntegerField(default=0, help_text='Set in $')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    url = models.SlugField(max_length=130, unique=True)
    draft = models.BooleanField(default=False)

    def __str__(self):
        return self.title
    def get_review(self):
        return self.reviews_set.filter(parent__isnull=True)

    def get_absolute_url(self):
        return reverse('movie_detail_url', kwargs={'slug': self.url})

    class Meta:
        verbose_name = 'Movie'
        verbose_name_plural = 'Movies'


class MovieShots(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=150, blank=True)
    image = models.ImageField(upload_to='movie_shots/')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Movie shot'
        verbose_name_plural = 'Movie shots'


class RatingStar(models.Model):
    value = models.SmallIntegerField(default=0)

    def __str__(self):
        return str(self.value)

    class Meta:
        verbose_name = 'Rating star'
        verbose_name_plural = 'Rating stars'


class Rating(models.Model):
    ip = models.CharField('IP address', max_length=15)
    star = models.ForeignKey(RatingStar, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, )

    def __str__(self):
        return f"{self.star} - {self.movie}"

    class Meta:
        verbose_name = 'Rating'
        verbose_name_plural = 'Ratings'


class Reviews(models.Model):
    email = models.EmailField()
    name = models.CharField(max_length=50)
    text = models.TextField(max_length=3000)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.name} - {self.movie}"

    class Meta:
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'
