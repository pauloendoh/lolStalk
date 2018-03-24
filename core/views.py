import requests
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

from core.forms import SignUpForm
from core.models import Summoner, Match, Summoner_Match

api_key = "RGAPI-d73fefa8-b18c-4044-ae0a-e53d985576db"


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
                new_summoner = Summoner.objects.create(region="na1", accountId=accountId, summonerId=summonerId, name=name, profileIconId=profileIconId, summonerLevel=summonerLevel, revisionDate=revisionDate)
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
                new_summoner = Summoner.objects.create(region="br1", accountId=accountId, summonerId=summonerId, name=name, profileIconId=profileIconId, summonerLevel=summonerLevel, revisionDate=revisionDate)
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
                new_summoner = Summoner.objects.create(region="kr", accountId=accountId, summonerId=summonerId,  name=name, profileIconId=profileIconId, summonerLevel=summonerLevel, revisionDate=revisionDate)
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
                new_summoner = Summoner.objects.create(region="euw1", accountId=accountId, name=name, profileIconId=profileIconId, summonerLevel=summonerLevel, revisionDate=revisionDate, summonerId=summonerId)
                summoners.append(new_summoner)

    return render(request, 'search.html', {"summoners": summoners})

def summoner(request, region, nickname):

    # Getting the summoner (and saving it in database)
    summoner = ""
    try:
        summoner = Summoner.objects.get(name__iexact=nickname, region__iexact=region)
    except:
        response = requests.get('https://' + region + '.api.riotgames.com/lol/summoner/v3/summoners/by-name/' + nickname + '?api_key=' + api_key)
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
        else: # If the summoner name doesn't exist in the region
            return redirect('home')

    response = requests.get(
        "https://" + region + ".api.riotgames.com/lol/match/v3/matchlists/by-account/" + str(summoner.accountId) + "/recent?api_key=" + api_key)
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
            timestamp = match["timestamp"]
            role = match["role"]
            summoner_match = Summoner_Match.objects.create(summoner_accountId=summoner.accountId, gameId=gameId, participantId=0, championId=championId, timestamp=timestamp, win=False, role=role, lane=lane, kills=0, deaths=0, assists=0)
            recent_matches.append(summoner_match)

    return render(request, 'summoner.html', {"summoner": summoner, "recent_matches": recent_matches, })


def summoner2(request, region, nickname):

    response = requests.get(
            'https://'+region+'.api.riotgames.com/lol/summoner/v3/summoners/by-name/' + nickname + '?api_key=' + api_key)
    summoner = response.json()

    if not 'accountId' in summoner:
        return redirect('home')

    account_id = str(summoner['accountId'])
    response = requests.get("https://"+region+".api.riotgames.com/lol/match/v3/matchlists/by-account/"+ account_id +"/recent?api_key="+api_key)
    recent_matches = response.json()

    detailed_matches = []

    for match in recent_matches["matches"]:

        game_id = str(match["gameId"])

        response = requests.get("https://" + region + ".api.riotgames.com/lol/match/v3/matches/" + game_id + "?api_key=" + api_key)
        detailed_match = response.json()

        for participantIdentity in detailed_match["participantIdentities"]:
            for key, value in participantIdentity["player"].items():
                if key == 'summonerName':
                    if value == nickname:
                        participantId = participantIdentity["participantId"]

                        # champion, win/lose and KDA
                        win = False
                        championId = 0
                        kills = 0
                        deaths = 0
                        assists = 0

                        # win/lose
                        for participant in detailed_match["participants"]:
                            if participant['participantId'] == participantId:
                                teamId = participant["teamId"]
                                for team in detailed_match["teams"]:
                                    if team["teamId"] == teamId:
                                        if not team["win"] == "Fail":
                                            win = True
                                championId = participant["championId"]
                                kills = participant["stats"]["kills"]
                                deaths = participant["stats"]["deaths"]
                                assists = participant["stats"]["assists"]

                        detailed_matches.append({"gameId": game_id, "participantId": participantId,  "win": win, "championId": championId, "kills": kills, "deaths": deaths, "assists": assists   })



    return render(request, 'summoner.html', {"region": region, "summoner": summoner, "matches":detailed_matches })