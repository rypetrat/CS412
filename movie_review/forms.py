from .models import *
from django import forms


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

class UpdateMovieForm(forms.ModelForm):
    '''Defines the form for updating a Movie.'''
    class Meta:
        model = Movie
        fields = ['genre', 'rating', 'director', 'release_date', 'description', 'poster_img', 'runtime']

class MovieFilterForm(forms.Form):
    # Filter by title
    title = forms.CharField(max_length=100, required=False, label="Title")
    # Filter by rating
    RATING_CHOICES = [(r, r) for r in Movie.objects.values_list('rating', flat=True).distinct()]
    rating = forms.ChoiceField(choices=[('', 'Any')] + RATING_CHOICES, required=False, label="Rating")
    # Filter by reviewer score range
    min_reviewer_score = forms.DecimalField(min_value=0, max_value=5, required=False, label="Minimum Reviewer Score")
    max_reviewer_score = forms.DecimalField(min_value=0, max_value=5, required=False, label="Maximum Reviewer Score")
    # Filter by release date
    release_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}), label="Release Date")
    # Filter by genre
    genre = forms.CharField(max_length=100, required=False, label="Genre")
    # Filter by runtime range
    min_runtime = forms.IntegerField(min_value=0, required=False, label="Minimum Runtime (minutes)")
    max_runtime = forms.IntegerField(min_value=0, required=False, label="Maximum Runtime (minutes)")

class ReviewerFilterForm(forms.Form):
    # Filter by title
    first_name = forms.CharField(max_length=100, required=False, label="First name")
    # Filter by title
    last_name = forms.CharField(max_length=100, required=False, label="Last name")