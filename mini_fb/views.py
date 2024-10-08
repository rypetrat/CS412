from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from .models import Profile, StatusMessage
from django.views.generic import ListView, DetailView, CreateView
from .forms import CreateProfileForm, CreateStatusMessageForm

class ShowAllProfilesView(ListView):
    '''Create a subclass of ListView to display all profiles'''
    model = Profile # retrieve objects of type Profile from the database
    template_name = 'mini_fb/show_all_profiles.html'
    context_object_name = 'profiles'

class ProfilePageView(DetailView):
    '''Show the details for one profile.'''
    model = Profile
    template_name = 'mini_fb/show_profile.html'
    context_object_name = 'profile'

class CreateProfileView(CreateView):
    '''handles profile creation'''
    model: Profile
    form_class = CreateProfileForm
    template_name = 'mini_fb/create_profile_form.html'

class CreateStatusMessageView(CreateView):
    '''Create a subclass of CreateView to handle profile creation'''
    model: StatusMessage
    form_class = CreateStatusMessageForm
    template_name = 'mini_fb/create_status_form.html'

    def get_context_data(self, **kwargs):
        # Get the context from the parent class
        context = super().get_context_data(**kwargs)
        profile_pk = self.kwargs['pk']
        context['profile'] = get_object_or_404(Profile, pk=profile_pk)  # Add Profile to context
        return context

    def form_valid(self, form):
        # Get the Profile object and set it on the StatusMessage
        profile_pk = self.kwargs['pk']
        profile = get_object_or_404(Profile, pk=profile_pk)
        status_message = form.save(commit=False)
        status_message.profile = profile  # Attach the Profile object
        status_message.save()
        return super().form_valid(form)

    def get_success_url(self):
        # Redirect to the profile page after successfully creating the status message
        return reverse('profile', kwargs={'pk': self.kwargs['pk']})