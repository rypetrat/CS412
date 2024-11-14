from django.contrib import admin

# Register your models here.
from .models import *
admin.site.register(Player)
admin.site.register(Champion)
admin.site.register(GameSession)
admin.site.register(PerformanceStat)