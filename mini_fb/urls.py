from django.urls import path
from .views import ShowAllProfilesView
from . import views

urlpatterns = [
    path('', views.ShowAllProfilesView.as_view(), name='show_all'), # generic class-based view
]