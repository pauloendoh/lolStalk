import datetime

import requests
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

from core.forms import SignUpForm
from core.models import Summoner, Match, Summoner_Match, Champion, Following

api_key = "RGAPI-f6567211-04e0-485e-9bd2-02b1b267fc3a"


def home(request):
    if not (request.user.is_authenticated):
        if request.method == 'POST':
            form = SignUpForm(request.POST)
            if form.is_valid():
                form.save()
                username = form.cleaned_data.get('username')
                raw_password = form.cleaned_data.get('password1')
                email = form.cleaned_data.get('email')
                user = authenticate(username=username, email=email, password=raw_password)
                auth_login(request, user)
                return redirect('home')
        else:
            form = UserCreationForm()
        return render(request, 'signup.html', {'form': form})

    summoner = {}
    if 'nickname' in request.GET:
        nickname = request.GET['nickname']
        region = request.GET['region']
        response = requests.get(
            'https://' + region + '.api.riotgames.com/lol/summoner/v3/summoners/by-name/' + nickname + '?api_key=' + api_key)
        summoner = response.json()
        summoner_id = summoner['id']

    return render(request, 'home.html', {"summoner": summoner})


def login(request):
    if request.user.is_authenticated:
        return redirect('home')
    return render(request, 'login.html')


def search(request):
    summoners = []
    if 'nickname' in request.GET:
        nickname = request.GET['nickname']

        found_summoners = Summoner.objects.filter(name__iexact=nickname)

        found_regions = []
        for summoner in found_summoners:
            found_regions.append(summoner.region)
            summoners.append(summoner)

        # make a http request for each other region (na1, br1, kr and euw1)
        if 'na1' not in found_regions:
            response = requests.get(
                'https://na1.api.riotgames.com/lol/summoner/v3/summoners/by-name/' + nickname + '?api_key=' + api_key)
            summoner = response.json()
            if 'accountId' in summoner:
                accountId = summoner["accountId"]
                summonerId = summoner["id"]

                name = summoner["name"]
                profileIconId = summoner["profileIconId"]
                summonerLevel = summoner["summonerLevel"]
                revisionDate = summoner["revisionDate"]
                new_summoner = Summoner.objects.create(region="na1", accountId=accountId, summonerId=summonerId,
                                                       name=name, profileIconId=profileIconId,
                                                       summonerLevel=summonerLevel, revisionDate=revisionDate)
                summoners.append(new_summoner)

        if 'br1' not in found_regions:
            response = requests.get(
                'https://br1.api.riotgames.com/lol/summoner/v3/summoners/by-name/' + nickname + '?api_key=' + api_key)
            summoner = response.json()
            if 'accountId' in summoner:
                accountId = summoner["accountId"]
                summonerId = summoner["id"]
                name = summoner["name"]
                profileIconId = summoner["profileIconId"]
                summonerLevel = summoner["summonerLevel"]
                revisionDate = summoner["revisionDate"]
                new_summoner = Summoner.objects.create(region="br1", accountId=accountId, summonerId=summonerId,
                                                       name=name, profileIconId=profileIconId,
                                                       summonerLevel=summonerLevel, revisionDate=revisionDate)
                summoners.append(new_summoner)

        if 'kr' not in found_regions:
            response = requests.get(
                'https://kr.api.riotgames.com/lol/summoner/v3/summoners/by-name/' + nickname + '?api_key=' + api_key)
            summoner = response.json()
            if 'accountId' in summoner:
                accountId = summoner["accountId"]
                summonerId = summoner["id"]
                name = summoner["name"]
                profileIconId = summoner["profileIconId"]
                summonerLevel = summoner["summonerLevel"]
                revisionDate = summoner["revisionDate"]
                new_summoner = Summoner.objects.create(region="kr", accountId=accountId, summonerId=summonerId,
                                                       name=name, profileIconId=profileIconId,
                                                       summonerLevel=summonerLevel, revisionDate=revisionDate)
                summoners.append(new_summoner)

        if 'euw1' not in found_regions:
            response = requests.get(
                'https://euw1.api.riotgames.com/lol/summoner/v3/summoners/by-name/' + nickname + '?api_key=' + api_key)
            summoner = response.json()
            if 'accountId' in summoner:
                accountId = summoner["accountId"]
                summonerId = summoner["id"]
                name = summoner["name"]
                profileIconId = summoner["profileIconId"]
                summonerLevel = summoner["summonerLevel"]
                revisionDate = summoner["revisionDate"]
                new_summoner = Summoner.objects.create(region="euw1", accountId=accountId, name=name,
                                                       profileIconId=profileIconId, summonerLevel=summonerLevel,
                                                       revisionDate=revisionDate, summonerId=summonerId)
                summoners.append(new_summoner)

    return render(request, 'search.html', {"summoners": summoners})


def summoner(request, region, nickname):
    # Getting the summoner (and saving it in database)
    summoner = ""
    try:
        summoner = Summoner.objects.get(name__iexact=nickname, region__iexact=region)
    except:
        response = requests.get(
            'https://' + region + '.api.riotgames.com/lol/summoner/v3/summoners/by-name/' + nickname + '?api_key=' + api_key)
        jsonresponse = response.json()
        if 'accountId' in jsonresponse:
            accountId = jsonresponse["accountId"]
            summonerId = jsonresponse["id"]
            name = jsonresponse["name"]
            profileIconId = jsonresponse["profileIconId"]
            summonerLevel = jsonresponse["summonerLevel"]
            revisionDate = jsonresponse["revisionDate"]
            summoner = Summoner.objects.create(region=region, accountId=accountId, name=name,
                                               profileIconId=profileIconId, summonerLevel=summonerLevel,
                                               revisionDate=revisionDate, summonerId=summonerId)
        else:  # If the summoner name doesn't exist in the region
            return redirect('home')

    response = requests.get(
        "https://" + region + ".api.riotgames.com/lol/match/v3/matchlists/by-account/" + str(
            summoner.accountId) + "/recent?api_key=" + api_key)
    jsonresponse = response.json()
    recent_matches = []

    for match in jsonresponse["matches"]:
        gameId = match["gameId"]
        try:
            summoner_match = Summoner_Match.objects.get(summoner_accountId=summoner.accountId, gameId=gameId)
            recent_matches.append(summoner_match)
        except:
            lane = match["lane"]
            championId = match["champion"]

            championName = Champion.objects.get(championId=championId).name

            timestamp = match["timestamp"]
            role = match["role"]

            participantId = 0
            summoner_name = ""
            win = False
            kills = 0
            deaths = 0
            assists = 0

            match_details = requests.get("https://" + region + ".api.riotgames.com/lol/match/v3/matches/" + str(
                gameId) + "?api_key=" + api_key).json()
            for participantIdentity in match_details["participantIdentities"]:
                if participantIdentity["player"]["summonerName"].lower() == summoner.name.lower():
                    participantId = participantIdentity["participantId"]
                    summoner_name = participantIdentity["player"]["summonerName"]

            # Save win/lose and KDA
            for participant in match_details["participants"]:
                if participantId == participant["participantId"]:
                    win = participant["stats"]["win"]
                    kills = participant["stats"]["kills"]
                    deaths = participant["stats"]["deaths"]
                    assists = participant["stats"]["assists"]

            summoner_match = Summoner_Match.objects.create(summoner_accountId=summoner.accountId,
                                                           summoner_name=summoner_name, gameId=gameId,
                                                           participantId=participantId, championId=championId,
                                                           championName=championName,
                                                           timestamp=timestamp, win=win, role=role, lane=lane,
                                                           kills=kills, deaths=deaths, assists=assists)
            recent_matches.append(summoner_match)


    # Check if user is following the summoner
    following = False
    if request.user.is_authenticated:
        user = request.user
        if Following.objects.filter(user=user, summoner=summoner).count()>0:
            following=True

    return render(request, 'summoner.html', {"summoner": summoner, "recent_matches": recent_matches, "following": following })


def champions(request):
    # Getting the most recent version of the static data
    response = requests.get("https://ddragon.leagueoflegends.com/api/versions.json").json()
    latest_version = response[0]

    # Saving champion data to database
    response = requests.get(
        "http://ddragon.leagueoflegends.com/cdn/" + latest_version + "/data/en_US/champion.json").json()
    if "data" in response:

        for champion, value in response["data"].items():
            print(value["name"] + ", " + value["title"])
            name = value["name"]
            championId = value["key"]
            locale = "en_US"

            Champion.objects.create(version=latest_version, name=name, championId=championId, locale=locale)

    return redirect('home')

@login_required
def follow(request, summoner_id):

    user = request.user
    summoner = Summoner.objects.get(summonerId=summoner_id)

    if Following.objects.filter(user=user, summoner=summoner).count() > 0:
        Following.objects.filter(user=user, summoner=summoner).delete()
    else:
        Following.objects.create(user=user, summoner=summoner)


    return redirect('home')