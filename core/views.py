import requests
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

from core.forms import SignUpForm

api_key = "RGAPI-749554e2-3874-4036-bf4a-b94d29aafd18"


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
        print("Summoner ID: " + str(summoner_id))

    return render(request, 'home.html', {"summoner": summoner})


def login(request):
    if request.user.is_authenticated:
        return redirect('home')
    return render(request, 'login.html')


def search(request):
    summoners = []
    if 'nickname' in request.GET:
        nickname = request.GET['nickname']

        # Getting summoner from BR1
        response = requests.get(
            'https://br1.api.riotgames.com/lol/summoner/v3/summoners/by-name/' + nickname + '?api_key=' + api_key)
        summoner = response.json()
        if 'accountId' in summoner:
            summoner['region'] = 'BR1'
            summoners.append(summoner)

        # Getting summoner from NA1
        response = requests.get(
            'https://na1.api.riotgames.com/lol/summoner/v3/summoners/by-name/' + nickname + '?api_key=' + api_key)
        summoner = response.json()
        if 'accountId' in summoner:
            summoner['region'] = 'NA1'
            summoners.append(summoner)

        return render(request, 'search.html', {"summoners": summoners})

def summoner(request, region, nickname):

    response = requests.get(
            'https://'+region+'.api.riotgames.com/lol/summoner/v3/summoners/by-name/' + nickname + '?api_key=' + api_key)
    summoner = response.json()
    if  not 'accountId' in summoner:
        return redirect('home')

    account_id = str(summoner['accountId'])
    response = requests.get("https://"+region+".api.riotgames.com/lol/match/v3/matchlists/by-account/"+ account_id +"/recent?api_key="+api_key)
    recent_matches = response.json()

    detailed_matches = {}

    for match in recent_matches["matches"]:

        game_id = str(match["gameId"])

        response = requests.get("https://" + region + ".api.riotgames.com/lol/match/v3/matches/" + game_id + "?api_key=" + api_key)
        detailed_matches = response.json()



    return render(request, 'summoner.html', {"region": region, "summoner": summoner, "matches":detailed_matches })