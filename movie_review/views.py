from typing import Any
from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from .models import *
from .forms import *
from django.views.generic import *
from django.contrib.auth import login
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

    def get_queryset(self):
        # Orders movies alphabetically by title
        return Movie.objects.all().order_by('title')

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
    
    def get_queryset(self):
        # Order movies alphabetically by last and then first name
        return Reviewer.objects.all().order_by('last_name', 'first_name')
    
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
    
    def get_queryset(self):
        # Order reviews by review_date in descending order
        return Review.objects.all().order_by('-review_date')

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
            # Save the user and link it to the reviewer
            user = user_creation_form.save()
            form.instance.user = user
            response = super().form_valid(form)
            # Log in the new user
            login(self.request, user)
            return response
        else:
            return self.form_invalid(form)
    
    def form_invalid(self, form):
        # Display errors for both forms
        context = self.get_context_data()
        context['user_creation_form'] = UserCreationForm(self.request.POST)
        context['form'] = form
        return self.render_to_response(context)
    
    def get_success_url(self):
        # redirect upon successful reviewer creation to that new reviewer's page
        return reverse('reviewer', kwargs={'pk': self.object.pk})

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
        # redirect upon successful creation of a new movie to that movie's page
        return reverse('movie', kwargs={'pk': self.object.pk})
    
class CreateReviewView(LoginRequiredMixin, CreateView):
    '''Handles review creation'''
    model = Review
    form_class = CreateReviewForm
    template_name = 'movie_review/create_review_form.html'
    
    def get_context_data(self, **kwargs):
        # Get the current user and their associated reviewer object
        user = self.request.user
        reviewer = Reviewer.objects.get(user=user)
        
        # Fetch movies already reviewed by this reviewer
        reviewed_movie_ids = Review.objects.filter(reviewer=reviewer).values_list('movie_id', flat=True)
        
        # Fetch movies not yet reviewed by this reviewer, ordered alphabetically by title
        movies_not_reviewed = Movie.objects.exclude(id__in=reviewed_movie_ids).order_by('title')
        
        # Add the filtered and sorted movies to the form's movie field queryset
        context = super().get_context_data(**kwargs)
        context['form'].fields['movie'].queryset = movies_not_reviewed
        context['movies'] = movies_not_reviewed
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
        # redirect upon successful creation of a new comment to the movie being reviewed's page
        return reverse('movie', kwargs={'pk': self.object.movie.pk})

class CreateWatchlistView(LoginRequiredMixin, CreateView):
    '''Handles watchlist creation/adding movies to a users watchlist'''
    model = Watchlist
    form_class = CreateWatchlistForm
    template_name = 'movie_review/create_watchlist_form.html'
    
    def get_context_data(self, **kwargs):
        # Get the current user and their associated reviewer object
        user = self.request.user
        reviewer = Reviewer.objects.get(user=user)
        
        # Fetch movies not in the reviewer's watchlist and sort them alphabetically by title
        movies_in_watchlist = Watchlist.objects.filter(reviewer=reviewer).values_list('movie', flat=True)
        available_movies = Movie.objects.exclude(id__in=movies_in_watchlist).order_by('title')
        
        # Add the sorted movies to the form's movie field queryset
        context = super().get_context_data(**kwargs)
        context['form'].fields['movie'].queryset = available_movies
        context['movies'] = available_movies
        return context
    
    def form_valid(self, form):
        reviewer = get_object_or_404(Reviewer, user=self.request.user)
        watchlist = form.save(commit=False)
        watchlist.reviewer = reviewer  # links to the reviewer
        watchlist.save()  # Save the watchlist with the linked reviewer 
        return super().form_valid(form)
    
    def get_success_url(self):
        # redirect to reviewer's page upon successful addition of a movie to watchlist
        return reverse('reviewer', kwargs={'pk': self.object.reviewer.pk})

class UpdateReviewerView(LoginRequiredMixin, UpdateView):
    '''Handles updating a Reviewer's profile.'''
    model = Reviewer
    form_class = UpdateReviewerForm
    template_name = 'movie_review/update_reviewer_form.html'

    def get_object(self):
        return get_object_or_404(Reviewer, user=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        reviewer = self.get_object()  
        context['first_name'] = reviewer.first_name  
        context['last_name'] = reviewer.last_name
        return context

    def get_success_url(self):
        return reverse('reviewer', kwargs={'pk': self.object.pk})

class DeleteReviewView(LoginRequiredMixin, DeleteView):
    '''Handles the deletion of a Review.'''
    model = Review
    template_name = 'movie_review/delete_review_form.html'
    context_object_name = 'review'

    def get_success_url(self):
        reviewer = get_object_or_404(Reviewer, user=self.request.user)
        return reverse('reviewer', kwargs={'pk': reviewer.pk})

class UpdateReviewView(LoginRequiredMixin, UpdateView):
    '''Handles the updating of a Review.'''
    model = Review
    form_class = UpdateReviewForm
    template_name = 'movie_review/update_review_form.html'
    context_object_name = 'review'

    def get_object(self, queryset=None):
        return get_object_or_404(Review, pk=self.kwargs['pk'])

    def get_success_url(self):
        return reverse('reviewer', kwargs={'pk': self.get_object().reviewer.pk})
    
class DeleteWatchlistView(LoginRequiredMixin, DeleteView):
    '''Handles the deletion of a Movie from a Watchlist.'''
    model = Watchlist
    template_name = 'movie_review/delete_watchlist_form.html'
    context_object_name = 'watchlist'

    def get_success_url(self):
        reviewer = get_object_or_404(Reviewer, user=self.request.user)
        return reverse('reviewer', kwargs={'pk': reviewer.pk})