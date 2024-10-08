from django.db import models
from django.urls import reverse

# Create your models here.
class Profile(models.Model):
    '''Encapsulate the idea of a profile'''
    firstName = models.CharField(max_length=100, blank=False)
    lastName = models.CharField(max_length=100, blank=False)
    city = models.CharField(max_length=100, blank=False)
    emailAddr = models.CharField(max_length=100, blank=False)
    ProfileImg = models.URLField(blank=True) 
    
    def __str__(self):
        '''Return a string representation of this Profile object.'''
        return f"{self.firstName} {self.lastName}'s profile "

    def get_statusMessages(self):
        '''Return all of the status messages about this profile.'''
        statusMessages = StatusMessage.objects.filter(profile=self)
        return statusMessages
    
    def get_absolute_url(self):
        # Returns the URL for a profile with its primary key
        return reverse('profile', kwargs={'pk': self.pk})

class StatusMessage(models.Model):
    '''Encapsulate the idea of a Status Messages on a Profile.'''
    
    # data attributes of a Status Message:
    profile = models.ForeignKey("Profile", on_delete=models.CASCADE)
    message = models.TextField(blank=False)
    timestamp = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        '''Return a string representation of this Status Message object.'''
        return f'{self.message}'