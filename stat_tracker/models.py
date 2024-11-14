from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

class Player(models.Model):
    '''Encapsulates the idea of a player's account'''
    account_name = None
    region = None
    rank = None
    profile_icon = None
    level = None

    def __str__(self):
        '''Return a string representation of this Player object'''
        return f"{self.account_name}'s account"

class Champion(models.Model):
    '''Encapsulates the idea of an in-game character'''
    name = None
    role = None
    icon = None
    winrate = None
    base_stats = None

    def __str__(self):
        '''Return a string representation of this Player object'''
        return f"Champion: {self.name}"

class GameSession(models.Model):
    '''Encapsulates the idea of a played game session'''
    player = None
    game_id = None
    date_played = None
    duration = None
    result = None

    def __str__(self):
        '''Return a string representation of this Player object'''
        return f"GameSession ID: {self.game_id}"

class PerformanceStat(models.Model):
    '''Encapsulates the idea of a players detailed in-game stats'''
    game_session = None
    champion = None
    kills = None
    deaths = None
    assists = None
    damage_dealt = None
    wards_placed = None

    def __str__(self):
        '''Return a string representation of this Player object'''
        return f"Performance Stats for GameSession ID: {self.game_session}"