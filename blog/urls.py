from django.urls import path
from .views import ShowAllView, RandomArticleView, ArticlePageView # our view class definition 
# from . import views
# from .models import Article
# from django.views.generic import ListView, DetailView
# import random

urlpatterns = [
    # map the URL (empty string) to the view
    path('', RandomArticleView.as_view(), name='random'), ## new
    path('show_all', ShowAllView.as_view(), name='show_all'),
    path('article/<int:pk>', ArticlePageView.as_view(), name='article'),
]