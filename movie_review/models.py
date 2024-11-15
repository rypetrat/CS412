from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Movie(models.Model):
    '''Encapsulates the idea of a Movie'''
    title = models.CharField(max_length=100, blank=False)
    genre = models.CharField(max_length=100, blank=False)
    release_date = models.DateField(blank=False)
    description = models.TextField(blank=False)
    poster_img = models.ImageField(upload_to='images/')
    runtime = models.IntegerField(blank=False)

    def __str__(self):
        '''Return a string representation of this Movie object'''
        return f"Movie: {self.title}"

class Review(models.Model):
    '''Encapsulates the idea of a Review on a Movie'''
    movie = models.ForeignKey("Movie", on_delete=models.CASCADE)
    review_message = models.TextField(blank=False)
    review_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        '''Return a string representation of this Review object'''
        return f"Review: {self.review_message}"

class Reviewer(models.Model):
    '''Encapsulates the idea of a person Reviewer'''
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, blank=False)
    last_name = models.CharField(max_length=100, blank=False)
    email = models.CharField(max_length=100, blank=False)
    profile_img = models.ImageField(upload_to='images/')
    joined_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        '''Return a string representation of this Reviewer object'''
        return f"Reviewer: {self.first_name} {self.last_name}"

class Rating(models.Model):
    '''Encapsulates the idea of a Rating on a Review'''
    review = models.ForeignKey("Review", on_delete=models.CASCADE)
    score = models.DecimalField(
        max_digits = 3,  
        decimal_places = 2,  
        blank = False,
        validators = [MinValueValidator(0), MaxValueValidator(5)])
    rating_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        '''Return a string representation of this Rating object'''
        return f"Rating for Review: {self.review.review_message}"