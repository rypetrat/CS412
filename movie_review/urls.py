from .views import *
from django.urls import path
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', ShowAllMovieView.as_view(), name='show_all'), # shows all movies
    path('movie/<int:pk>/', MoviePageView.as_view(), name='movie'), # shows a single movie
    path('movie_search/', MovieListView.as_view(), name='movie_search'), # form for searching for a movie
    path('reviewer_search/', ReviewerListView.as_view(), name='reviewer_search'), # form for searching for a reviewer
    path('reviewers/', ShowAllReviewerView.as_view(), name='show_all_reviewers'), # shows all reviewers
    path('reviewer/<int:pk>/', ReviewerPageView.as_view(), name='reviewer'), # shows a single reviewer
    path('reviews/', ShowAllReviewView.as_view(), name='show_all_reviews'), # shows all reviews
    path('create_reviewer/', CreateReviewerView.as_view(), name='create_reviewer'), # form for creating new reviewer
    path('create_review/', CreateReviewView.as_view(), name='create_review'), # form for creating a new review
    path('add_movie/', CreateMovieView.as_view(), name='add_movie'), # form for creating a new movie
    path('add_to_watchlist/', CreateWatchlistView.as_view(), name='add_to_watchlist'), # form for adding a movie to a users watchlist
    path('reviewer/update/', UpdateReviewerView.as_view(), name='update_reviewer'), # form for updating a reviewer profile
    path('review/<int:pk>/delete/', DeleteReviewView.as_view(), name='delete_review'), # form for deleting a review
    path('review/<int:pk>/update/', UpdateReviewView.as_view(), name='update_review'), # form for updating a review
    path('movie/<int:pk>/update/', UpdateMovieView.as_view(), name='update_movie'), # form for updating a movie
    path('watchlist/<int:pk>/delete/', DeleteWatchlistView.as_view(), name='delete_watchlist'), # form for deleting a watchlist entry
    path('login/', auth_views.LoginView.as_view(template_name='movie_review/login.html'), name='login'), # handles login
    path('logout/', auth_views.LogoutView.as_view(template_name='movie_review/logged_out.html', next_page='show_all'), name='logout'), # handles logout
]