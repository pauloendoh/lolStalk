import datetime

import requests

from core.models import Following, Summoner, League, Summoner_Match, Champion

api_key = "RGAPI-8d37ff73-f42d-4457-8a55-bf8ddf3a8ac1"


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
        jsonresponse = requests.get(
            'https://' + region + '.api.riotgames.com/lol/summoner/v3/summoners/by-name/' + nickname + '?api_key=' + api_key).json()
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
                                               revisionDate=revisionDate, summonerId=summonerId,
                                               leagues_updated_at=datetime.datetime.now())

        # If the nickname doesn't exist in the region
        else:
            print("Summoner '" + nickname + "' doesn't exist in " + region)
            return None

    return summoner


def get_leagues(summoner):
    leagues = []

    # I HAVE TO CREATE A CONDITIONAL STATEMENT:
    # if lastUpdated < 1h, then get from database
    # else, update database using Riot API

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
            if "miniSeries" in league_data:
                print("The summoner " + league.summoner.name + "is in a miniseries for the queue " + league.queueType)
                league.miniSeries = league_data["miniSeries"]["progress"]

            League.objects.filter(summoner=summoner, queueType=league.queueType).delete()

            league.save()
            leagues.append(league)

    return leagues


# Recent matches
def get_recent_matches(summoner):
    recent_matches = []

    # Getting a list of the summoner's recent matches
    jsonresponse = requests.get(
        "https://" + summoner.region + ".api.riotgames.com/lol/match/v3/matchlists/by-account/" + str(
            summoner.accountId) + "/recent?api_key=" + api_key).json()

    # If the player haven't been playing...
    # I HAVE TO IMPROVE THIS!!!
    if "status" in jsonresponse:
        return None

    # Using the data of the list of the recent matches.
    # It will check detailed info of each match, eventually
    for match in jsonresponse["matches"]:
        gameId = match["gameId"]

        # Check if summoner already has information about this match,
        # so it doesn't have to create a new one
        try:
            summoner_match = Summoner_Match.objects.get(summoner_accountId=summoner.accountId, gameId=gameId)
            recent_matches.append(summoner_match)
        except:
            lane = match["lane"]
            championId = match["champion"]
            championName = Champion.objects.get(championId=championId).name
            timestamp = datetime.datetime.fromtimestamp(match["timestamp"] / 1e3)
            role = match["role"]

            participantId = 0
            win = False
            kills = 0
            deaths = 0
            assists = 0

            # Getting detailed info of each match
            # in the list of recent matches
            match_details = requests.get(
                "https://" + summoner.region + ".api.riotgames.com/lol/match/v3/matches/" + str(
                    gameId) + "?api_key=" + api_key).json()
            for participantIdentity in match_details["participantIdentities"]:
                if participantIdentity["player"]["summonerName"].lower() == summoner.name.lower():
                    participantId = participantIdentity["participantId"]

                    # Save win/lose and KDA
                    for participant in match_details["participants"]:
                        if participantId == participant["participantId"]:
                            win = participant["stats"]["win"]
                            kills = participant["stats"]["kills"]
                            deaths = participant["stats"]["deaths"]
                            assists = participant["stats"]["assists"]

                    summoner_match = Summoner_Match.objects.create(summoner_accountId=summoner.accountId,
                                                                   summoner_name=summoner.name, gameId=gameId,
                                                                   participantId=participantId, championId=championId,
                                                                   championName=championName,
                                                                   timestamp=timestamp, win=win, role=role, lane=lane,
                                                                   kills=kills, deaths=deaths, assists=assists)
                    recent_matches.append(summoner_match)

    return recent_matches


def user_is_following(request, summoner):
    is_following = False

    if request.user.is_authenticated:
        user = request.user
        if Following.objects.filter(user=user, summoner=summoner).count() > 0:
            following = True

    return is_following


def api_key_is_updated():
    # Making a test request using Hide on Bush's account
    jsonresponse = requests.get(
        'https://kr.api.riotgames.com/lol/summoner/v3/summoners/4460427?api_key=' + api_key).json()

    if "status" in jsonresponse:
        return False

    return True


def get_latest_static_data_version():
    response = requests.get("https://ddragon.leagueoflegends.com/api/versions.json").json()
    return response[0]


def get_timeline(user):
    # Timeline is a list of matches
    # of the summoners that the user follows.
    # The timeline is ordered by time (newest first).
    timeline = []

    following_list = Following.objects.filter(user=user)

    for following in following_list:
        account_id = following.summoner.accountId
        summoner_match_list = Summoner_Match.objects.filter(summoner_accountId=account_id)

        for summoner_match in summoner_match_list:
            timeline.append(summoner_match)
        timeline.sort(key=lambda object1: object1.timestamp, reverse=True)

    return timeline
