## hw/urls.py
## app-specific URLs for the hw application

from django.urls import path
from django.conf import settings
from . import views 

# list of URLs for this app:
urlpatterns = [
    path(r'', views.home, name="home") ## function should match name
]

