from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Movie(models.Model):
    '''Encapsulates the idea of a Movie'''
    title = models.CharField(max_length=100, blank=False)
    genre = models.CharField(max_length=100, blank=False)
    rating = models.CharField(max_length=5, blank=False)
    director = models.CharField(max_length=100, blank=False)
    release_date = models.DateField(blank=False)
    description = models.TextField(blank=False)
    poster_img = models.ImageField(upload_to='images/')
    runtime = models.IntegerField(blank=False)

    def __str__(self):
        '''Return a string representation of this Movie object'''
        return f"{self.title}"

class Review(models.Model):
    '''Encapsulates the idea of a Review on a Movie'''
    movie = models.ForeignKey("Movie", on_delete=models.CASCADE)
    reviewer = models.ForeignKey("Reviewer", on_delete=models.CASCADE)
    review_message = models.TextField(blank=False)
    review_score = models.DecimalField(max_digits = 3, decimal_places = 2, blank = False, 
            validators = [MinValueValidator(0), MaxValueValidator(5)])
    review_date = models.DateTimeField(auto_now=True, blank=False)

    def __str__(self):
        '''Return a string representation of this Review object'''
        return f"{self.reviewer}'s review of {self.movie}"

class Reviewer(models.Model):
    '''Encapsulates the idea of a person Reviewer'''
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, blank=False)
    last_name = models.CharField(max_length=100, blank=False)
    email = models.CharField(max_length=100, blank=False)
    profile_img = models.ImageField(upload_to='images/')
    joined_date = models.DateTimeField(auto_now=True, blank=False)

    def __str__(self):
        '''Return a string representation of this Reviewer object'''
        return f"{self.first_name} {self.last_name}"

class Watchlist(models.Model):
    '''Encapsulates the idea of a Watchlist for a Reviewer'''
    reviewer = models.ForeignKey("Reviewer", on_delete=models.CASCADE)
    movie = models.ForeignKey("Movie", on_delete=models.CASCADE)
    added_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        '''Return a string representation of this Watchlist entry'''
        return f"{self.reviewer} watched: {self.movie.title}"