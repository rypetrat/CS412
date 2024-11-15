from django.urls import path
from .views import *
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', ShowAllMovieView.as_view(), name='show_all'),
]