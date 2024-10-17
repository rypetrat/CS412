from django import forms
from .models import *

class CreateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['firstName', 'lastName', 'city', 'emailAddr', 'ProfileImg']

class CreateStatusMessageForm(forms.ModelForm):
    class Meta:
        model = StatusMessage
        fields = ['message']

class UpdateProfileForm(forms.ModelForm):
    '''Form to update the Profile, excluding first and last name.'''
    class Meta:
        model = Profile
        fields = ['city', 'emailAddr', 'ProfileImg']

class UpdateStatusMessageForm(forms.ModelForm):
    '''Form to update the status message.'''
    class Meta:
        model = StatusMessage
        fields = ['message']