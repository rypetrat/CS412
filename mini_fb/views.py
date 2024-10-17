# Create your views here.
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from .models import *
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .forms import *

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
    '''Create a subclass of CreateView to handle status message creation'''
    model = StatusMessage
    form_class = CreateStatusMessageForm
    template_name = 'mini_fb/create_status_form.html'

    def get_context_data(self, **kwargs):
        # Get the context from the parent class
        context = super().get_context_data(**kwargs)
        profile_pk = self.kwargs['pk']
        context['profile'] = get_object_or_404(Profile, pk=profile_pk)
        return context

    def form_valid(self, form):
        # Get the Profile object and set it on the StatusMessage
        profile_pk = self.kwargs['pk']
        profile = get_object_or_404(Profile, pk=profile_pk)
        
        # Save the status message and commit to database
        status_message = form.save(commit=False)
        status_message.profile = profile
        status_message.save()
        
        # Handle file upload
        files = self.request.FILES.getlist('images') 
        for file in files:
            Image.objects.create(status_message=status_message, image_file=file)
        
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('profile', kwargs={'pk': self.kwargs['pk']})
    
class UpdateProfileView(UpdateView):
    '''View to handle updating a user's profile.'''
    model = Profile
    form_class = UpdateProfileForm
    template_name = 'mini_fb/update_profile_form.html'

    def get_object(self, queryset=None):
        return get_object_or_404(Profile, pk=self.kwargs['pk'])
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.get_object()  
        context['first_name'] = profile.firstName  
        context['last_name'] = profile.lastName
        return context

    def get_success_url(self):
        return reverse('profile', kwargs={'pk': self.kwargs['pk']})
    
class DeleteStatusMessageView(DeleteView):
    '''View to handle the deletion of a status message.'''
    model = StatusMessage
    template_name = 'mini_fb/delete_status_form.html'
    context_object_name = 'status_message'

    def get_success_url(self):
        return reverse('profile', kwargs={'pk': self.object.profile.pk})
    
class UpdateStatusMessageView(UpdateView):
    '''View to handle updating a status message.'''
    model = StatusMessage
    form_class = UpdateStatusMessageForm
    template_name = 'mini_fb/update_status_form.html'
    context_object_name = 'status_message'

    def get_success_url(self):
        # Redirect to the profile page after successful update
        return reverse('profile', kwargs={'pk': self.object.profile.pk})