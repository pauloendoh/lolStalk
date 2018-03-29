import datetime

import requests
from django.shortcuts import redirect

from core.models import Following, Summoner, League

api_key = "RGAPI-16db827d-ecff-42af-9ae7-111b9c5482ed"


def get_timeline(user):
    timeline = []

    following_list = Following.objects.filter(user=user)
    for following in following_list:
        account_id = following.summoner.accountId

    return timeline


# Use the region and nickname to get
# the updated summoner
def get_summoner(region, nickname):
    summoner = None

    # Checking if summoner already exists in the database
    try:
        summoner = Summoner.objects.get(name__iexact=nickname, region__iexact=region)

    # If summoner doesn't exist in the database,
    # get info from Riot API and store it
    except:
        jsonresponse = requests.get('https://' + region + '.api.riotgames.com/lol/summoner/v3/summoners/by-name/' + nickname + '?api_key=' + api_key).json()
        if 'accountId' in jsonresponse:
            accountId = jsonresponse["accountId"]
            summonerId = jsonresponse["id"]
            name = jsonresponse["name"]
            profileIconId = jsonresponse["profileIconId"]
            summonerLevel = jsonresponse["summonerLevel"]
            revisionDate = jsonresponse["revisionDate"]

            # Finally, the summoner is created
            # (or replaces with a new nickname)
            Summoner.objects.filter(region=region, accountId=accountId, summonerId=summonerId).delete()
            summoner = Summoner.objects.create(region=region, accountId=accountId, name=name,
                                               profileIconId=profileIconId, summonerLevel=summonerLevel,
                                               revisionDate=revisionDate, summonerId=summonerId, leagues_updated_at=datetime.datetime.now())

        # If the nickname doesn't exist in the region
        else:
            print("Summoner '" + nickname + "' doesn't exist in " + region)

    return summoner


def get_leagues(summoner):
    leagues = []

    # Using Riot API to get summoner's leagues info
    # (by region and summoner_id)
    jsonresponse = requests.get(
        "https://" + summoner.region + ".api.riotgames.com/lol/league/v3/positions/by-summoner/" + str(
            summoner.summonerId) + "?api_key=" + api_key).json()
    if not "status" in jsonresponse:
        for league_data in jsonresponse:
            league = League()

            league.summoner = summoner
            league.queueType = league_data["queueType"]
            league.tier = league_data["tier"]
            league.rank = league_data["rank"]
            league.leaguePoints = league_data["leaguePoints"]
            league.wins = int(league_data["wins"])
            league.losses = int(league_data["losses"])
            league.miniSeries = ""

            League.objects.filter(summoner=summoner, queueType=league.queueType).delete()

            league.save()
            leagues.append(league)

    return leagues
