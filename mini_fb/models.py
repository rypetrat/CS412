from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

class Profile(models.Model):
    '''Encapsulate the idea of a profile'''
    user = models.ForeignKey(User, on_delete=models.CASCADE)
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
    
    def get_friends(self):
        friends_as_profile1 = Friend.objects.filter(profile1=self)
        friends_as_profile2 = Friend.objects.filter(profile2=self)

        friends = [friend.profile2 for friend in friends_as_profile1] + \
                  [friend.profile1 for friend in friends_as_profile2]
        return friends
    
    def get_absolute_url(self):
        return reverse('profile', kwargs={'pk': self.pk})
    
    def add_friend(self, other):
        existing_friend = Friend.objects.filter(
            (models.Q(profile1=self) & models.Q(profile2=other)) | 
            (models.Q(profile1=other) & models.Q(profile2=self))
        ).exists()
        if not existing_friend:
            new_friend = Friend(profile1=self, profile2=other)
            new_friend.save()
    
    def get_friend_suggestions(self):
        friend_ids = Friend.objects.filter(
            models.Q(profile1=self) | models.Q(profile2=self)
        ).values_list('profile1', 'profile2')

        flat_friend_ids = {friend_id for pair in friend_ids for friend_id in pair}
        flat_friend_ids.discard(self.pk)

        suggested_friends = Profile.objects.exclude(pk__in=flat_friend_ids).exclude(pk=self.pk)

        return suggested_friends
    
    def get_news_feed(self):
        friend_ids = [friend.pk for friend in self.get_friends()]
        all_profile_ids = [self.pk] + friend_ids
        
        news_feed = StatusMessage.objects.filter(
            models.Q(profile__in=all_profile_ids)
        ).order_by('-timestamp')
        
        return news_feed

class StatusMessage(models.Model):
    '''Encapsulate the idea of a Status Messages on a Profile.'''
    
    profile = models.ForeignKey("Profile", on_delete=models.CASCADE)
    message = models.TextField(blank=False)
    timestamp = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        '''Return a string representation of this Status Message object.'''
        return f'{self.message}'
    
    def get_images(self):
        '''Return all images associated with this Status Message.'''
        return Image.objects.filter(status_message=self)
    
class Image(models.Model):
    status_message = models.ForeignKey("StatusMessage", on_delete=models.CASCADE, related_name='images')
    image_file = models.ImageField(upload_to='images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.status_message.message}"
    
class Friend(models.Model):
    '''Encapsulate the idea of a Friend.'''
    profile1 = models.ForeignKey(Profile, related_name='friend1', on_delete=models.CASCADE)
    profile2 = models.ForeignKey(Profile, related_name='friend2', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.profile1} & {self.profile2}"