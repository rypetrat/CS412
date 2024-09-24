## hw/urls.py
## app-specific URLs for the hw application

from django.urls import path
from django.conf import settings
from . import views 

urlpatterns = [
    path('', views.main, name="main"),  # handles requests to the root URL
    path('quote/', views.quotes, name="quotes"),  # handles requests to quote
    path('show_all/', views.show_all, name="quotes"), # handles requests to show all
    path('about/', views.about, name="quotes"), # handles requests to about
]

