from django.contrib import admin

# Register your models here.
from .models import *
admin.site.register(Movie)
admin.site.register(Review)
admin.site.register(Reviewer)
admin.site.register(Rating)