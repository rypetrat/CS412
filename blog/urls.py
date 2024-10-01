from django.urls import path
from .views import ShowAllView # our view class definition 
from . import views
urlpatterns = [
    # map the URL (empty string) to the view
    path('', views.ShowAllView.as_view(), name='show_all'), # generic class-based view
]