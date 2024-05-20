from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import Avg

class Genre(models.Model):
    name=models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Job(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Person(models.Model):
    name = models.CharField(max_length=128)
    tmdb_id = models.IntegerField(unique=True, null=True, blank=True)
    profile_path = models.URLField(blank=True, null=True)
    biography = models.TextField(blank=True, null=True)
    birthday = models.DateField(null=True, blank=True)
    deathday = models.DateField(null=True, blank=True)
    place_of_birth = models.CharField(max_length=256, blank=True, null=True)

    def __str__(self):
        return self.name



class Movie(models.Model):
    title = models.CharField(max_length=200)
    overview = models.TextField()
    release_date = models.DateTimeField(blank=True)
    running_time = models.IntegerField(blank=True) 
    budget = models.IntegerField(blank=True)
    tmdb_id = models.IntegerField(blank=True,unique=True, null=True)
    revenue = models.IntegerField(blank=True)
    poster_path = models.URLField(blank=True)
    genres = models.ManyToManyField(Genre) 
    credits = models.ManyToManyField(Person, through="MovieCredit")

    def __str__(self):
        return self.title + " " + str(self.release_date.year)
        
    def average_rating(self):
        return self.moviereview_set.aggregate(Avg('rating'))['rating__avg'] or 0


class MovieCredit(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)


class MovieReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1),
                                                          MaxValueValidator(100)])
    review = models.TextField(blank=True)