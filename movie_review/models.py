from django.db import models
from django.db.models import Avg
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
    
    def get_reviews(self):
        '''Return all of the Reviews on this Movie.'''
        reviews = Review.objects.filter(movie=self)
        return reviews
    
    def get_watched(self):
        '''Returns all the people who have this movie in their Watchlist.'''
        watched = Reviewer.objects.filter(id__in=Watchlist.objects.filter(movie=self).values('reviewer'))
        return watched
    
    def average_rating(self):
        """Calculate the average review score for the movie."""
        return self.get_reviews().aggregate(average=Avg('review_score'))['average'] or 0

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
    
    def get_reviews(self):
        '''Return all of the Reviews from this Reviewer.'''
        reviews = Review.objects.filter(reviewer=self)
        return reviews
    
    def get_watchlist(self):
        '''Returns the watchlist of this Reviewer.'''
        watchlist = Watchlist.objects.filter(reviewer=self)
        return watchlist
    
    def average_rating(self):
        """Calculate the average score of all reviews given by the reviewer."""
        return self.get_reviews().aggregate(average=Avg('review_score'))['average'] or 0

class Watchlist(models.Model):
    '''Encapsulates the idea of a Watchlist for a Reviewer'''
    reviewer = models.ForeignKey("Reviewer", on_delete=models.CASCADE)
    movie = models.ForeignKey("Movie", on_delete=models.CASCADE)
    added_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        '''Return a string representation of this Watchlist entry'''
        return f"{self.reviewer} watched: {self.movie.title}"