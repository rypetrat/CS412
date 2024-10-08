from django.urls import path
from .views import ShowAllProfilesView, ProfilePageView, CreateProfileView, CreateStatusMessageView
from . import views

urlpatterns = [
    path('', ShowAllProfilesView.as_view(), name='show_all'),
    path('profile/<int:pk>', ProfilePageView.as_view(), name='profile'),
    path('create_profile', CreateProfileView.as_view(), name='create_profile'),
    path('profile/<int:pk>/create_status', CreateStatusMessageView.as_view(), name='create_status'),
]