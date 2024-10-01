from django.db import models

# Create your models here.
class Profile(models.Model):
    '''Encapsulate the idea of a profile'''
    firstName = models.TextField(blank=False)
    lastName = models.TextField(blank=False)
    city = models.TextField(blank=False)
    emailAddr = models.TextField(blank=False)
    ProfileImg = models.URLField(blank=True) 
    
    def __str__(self):
        '''Return a string representation of this Article object.'''
        return f"{self.firstName} {self.lastName}'s profile "