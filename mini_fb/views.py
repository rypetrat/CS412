# Create your views here.
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from .models import *
from django.views.generic import *
from .forms import *

class ShowAllProfilesView(ListView):
    '''Create a subclass of ListView to display all profiles'''
    model = Profile
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
        context = super().get_context_data(**kwargs)
        profile_pk = self.kwargs['pk']
        context['profile'] = get_object_or_404(Profile, pk=profile_pk)
        return context

    def form_valid(self, form):
        profile_pk = self.kwargs['pk']
        profile = get_object_or_404(Profile, pk=profile_pk)
        
        status_message = form.save(commit=False)
        status_message.profile = profile
        status_message.save()
        
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
        return reverse('profile', kwargs={'pk': self.object.profile.pk})
    
class CreateFriendView(View):
    def dispatch(self, request, *args, **kwargs):
        profile_pk = kwargs['pk']
        friend_pk = kwargs['other_pk']

        profile = get_object_or_404(Profile, pk=profile_pk)
        friend_profile = get_object_or_404(Profile, pk=friend_pk)

        profile.add_friend(friend_profile)

        return redirect('profile', pk=profile_pk)
    
class ShowFriendSuggestionsView(DetailView):
    model = Profile
    template_name = 'mini_fb/friend_suggestions.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.get_object()
        context['friend_suggestions'] = profile.get_friend_suggestions()
        return context
    
class ShowNewsFeedView(DetailView):
    model = Profile
    template_name = 'mini_fb/news_feed.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['news_feed'] = self.object.get_news_feed()
        return context