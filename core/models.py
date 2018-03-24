from django.db import models


class Summoner(models.Model):
    accountId = models.IntegerField()
    summonerId = models.IntegerField()
    region = models.CharField(max_length=5)
    name = models.CharField(max_length=18)
    profileIconId = models.IntegerField()
    revisionDate = models.FloatField()
    summonerLevel = models.IntegerField()


class Summoner_Match(models.Model):
    summoner_accountId = models.IntegerField()
    gameId = models.FloatField()
    participantId = models.IntegerField()
    timestamp = models.FloatField()
    championId = models.IntegerField()
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
