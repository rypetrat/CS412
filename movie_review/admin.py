from django.contrib import admin

# Register the models for the admin.
from .models import *
admin.site.register(Movie)
admin.site.register(Review)
admin.site.register(Reviewer)
admin.site.register(Watchlist)