from django.contrib.auth.models import User
from django.db import models


class Summoner(models.Model):
    accountId = models.IntegerField()
    summonerId = models.IntegerField()
    region = models.CharField(max_length=5)
    name = models.CharField(max_length=18)
    profileIconId = models.IntegerField()
    revisionDate = models.FloatField()
    summonerLevel = models.IntegerField()
    leagues_updated_at = models.DateTimeField()


class Summoner_Match(models.Model):
    summoner_accountId = models.IntegerField()
    summoner_name = models.CharField(max_length=18)
    gameId = models.FloatField()
    participantId = models.IntegerField()
    timestamp = models.DateTimeField()
    championId = models.IntegerField()
    championName = models.CharField(max_length=25)
    win = models.BooleanField()
    role = models.CharField(max_length=25)
    lane = models.CharField(max_length=25)
    kills = models.IntegerField()
    deaths = models.IntegerField()
    assists = models.IntegerField()


class Match(models.Model):
    gameId = models.FloatField()
    gameCreation = models.FloatField()
    gameDuration = models.FloatField()

class Champion(models.Model):
    championId = models.CharField(max_length=10)
    name = models.CharField(max_length=25)
    locale = models.CharField(max_length=10)
    version = models.CharField(max_length=25)

class Following(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    summoner = models.ForeignKey(Summoner, on_delete=models.CASCADE)

class League(models.Model):
    summoner = models.ForeignKey(Summoner, on_delete=models.CASCADE)

    queueType = models.TextField()
    tier = models.TextField()
    rank = models.TextField()
    leaguePoints = models.IntegerField()
    wins = models.IntegerField
    losses = models.IntegerField
    miniSeries = models.TextField()
