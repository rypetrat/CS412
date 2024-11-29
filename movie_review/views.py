from typing import Any
from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from .models import *
from .forms import *
from django.views.generic import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm


class ShowAllMovieView(ListView):
    '''Create a subclass of ListView to display all Movies'''
    model = Movie
    template_name = 'movie_review/show_all_movies.html'
    context_object_name = 'movies'

    def dispatch(self, *args, **kwargs):
        print(f"self.request.user={self.request.user}")
        return super().dispatch(*args, **kwargs)

class MoviePageView(DetailView):
    '''Show the full details for a single movie.'''
    model = Movie
    template_name = 'movie_review/show_movie.html'
    context_object_name = 'movie'

    def get_reviews(self):
        '''Return all of the reviews for this movie.'''
        reviews = Review.objects.filter(profile=self)
        return reviews

class ShowAllReviewerView(ListView):
    '''Create a subclass of ListView to display all Movies'''
    model = Reviewer
    template_name = 'movie_review/show_all_reviewers.html'
    context_object_name = 'reviewers'

    def dispatch(self, *args, **kwargs):
        print(f"self.request.user={self.request.user}")
        return super().dispatch(*args, **kwargs)
    
class ReviewerPageView(DetailView):
    '''Show the full details for a single movie.'''
    model = Reviewer
    template_name = 'movie_review/show_reviewer.html'
    context_object_name = 'reviewer'

class ShowAllReviewView(ListView):
    '''Create a subclass of ListView to display all Movies'''
    model = Review
    template_name = 'movie_review/show_all_reviews.html'
    context_object_name = 'reviews'

    def dispatch(self, *args, **kwargs):
        print(f"self.request.user={self.request.user}")
        return super().dispatch(*args, **kwargs)

class CreateReviewerView(CreateView):
    '''Handles Reviewer creation'''
    model = Reviewer
    form_class = CreateReviewerForm
    template_name = 'movie_review/create_reviewer_form.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_creation_form'] = UserCreationForm()
        return context

    def form_valid(self, form):
        user_creation_form = UserCreationForm(self.request.POST)
        if user_creation_form.is_valid():
            user = user_creation_form.save()
            form.instance.user = user
            return super().form_valid(form)
        else:
            return self.form_invalid(form)
    
    def get_success_url(self):
        return reverse('', kwargs={'pk': self.object.pk})

class CreateMovieView(CreateView):
    '''Handles movie creation'''
    model = Movie
    form_class = CreateMovieForm
    template_name = 'movie_review/create_movie_form.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_creation_form'] = UserCreationForm()
        return context

    def form_valid(self, form):
        # Save the movie instance
        movie = form.save(commit=False)
        movie.save()

        # Handle uploaded poster image
        if 'poster_img' in self.request.FILES:
            movie.poster_img = self.request.FILES['poster_img']
            movie.save()

        # Call the parent class's form_valid to complete processing
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('movie', kwargs={'pk': self.object.pk})
    
class CreateReviewView(CreateView):
    '''Handles review creation'''
    model = Review
    form_class = CreateReviewForm
    template_name = 'movie_review/create_review_form.html'
    
    def get_context_data(self, **kwargs):
        # Make sure to include a list of movies in the context so the user can select one
        context = super().get_context_data(**kwargs)
        context['movies'] = Movie.objects.all()  # Fetch all movies to populate the movie selection field
        return context

    def form_valid(self, form):
        # Get the movie from the form
        movie = form.cleaned_data['movie']

        # Ensure that a reviewer exists for the user
        user = self.request.user
        reviewer = Reviewer.objects.get(user=user)

        # Create the review
        review = form.save(commit=False)
        review.movie = movie
        review.reviewer = reviewer
        review.save()
        
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('movie', kwargs={'pk': self.object.movie.pk})