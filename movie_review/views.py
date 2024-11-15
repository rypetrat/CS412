from typing import Any
from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from .models import *
from django.views.generic import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm


class ShowAllMovieView(ListView):
    '''Create a subclass of ListView to display all Movies'''
    model = Movie
    template_name = 'movie_review/base.html'
    context_object_name = 'movies'