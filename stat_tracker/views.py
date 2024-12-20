from typing import Any
from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from .models import *
from django.views.generic import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
# Create your views here.


class ShowAllPlayerView(ListView):
    '''Create a subclass of ListView to display all players'''
    model = Player
    template_name = 'stat_tracker/base.html'
    context_object_name = 'players'