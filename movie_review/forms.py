from django import forms
from .models import *

class CreateReviewerForm(forms.ModelForm):
    ''' Defnies the form to create a new Reviewer '''
    class Meta:
        model = Reviewer
        fields = ['first_name', 'last_name', 'email', 'profile_img']

class CreateReviewForm(forms.ModelForm):
    ''' Defines the form for creating a new Review '''
    class Meta:
        model = Review
        fields = ['movie', 'review_message', 'review_score']

class UpdateReviewForm(forms.ModelForm):
    ''' Defines the form for updating a Review '''
    class Meta:
        model = Review
        fields = ['review_message', 'review_score']

class CreateMovieForm(forms.ModelForm):
    ''' Defines the form for creating a new Movie '''
    class Meta:
        model = Movie
        fields = ['title', 'genre', 'rating', 'director', 'release_date', 'description', 'poster_img', 'runtime']

class CreateWatchlistForm(forms.ModelForm):
    ''' Defines the form for adding a new movie to a Reviewer's Watchlist '''
    class Meta:
        model = Watchlist
        fields = ['movie']

class UpdateReviewerForm(forms.ModelForm):
    '''Defines the form for updating a Reviewer's profile'''
    class Meta:
        model = Reviewer
        fields = ['email', 'profile_img']

class UpdateReviewForm(forms.ModelForm):
    '''Defines the form for updating a Review.'''
    class Meta:
        model = Review
        fields = ['review_message', 'review_score']
