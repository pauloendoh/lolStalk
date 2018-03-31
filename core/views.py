import datetime

import requests
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

from core.forms import SignUpForm
from core.functions import get_summoner, get_leagues, get_recent_matches, user_is_following, api_key_is_updated, \
    get_latest_static_data_version, get_timeline
from core.models import Summoner, Match, Summoner_Match, Champion, Following, League


def home(request):
    if not request.user.is_authenticated:

        # If a sign up form was submitted
        if request.method == 'POST':
            form = SignUpForm(request.POST)
            if form.is_valid():

                # Create a new user, then sign in automatically
                form.save()
                username = form.cleaned_data.get('username')
                raw_password = form.cleaned_data.get('password1')
                email = form.cleaned_data.get('email')
                user = authenticate(username=username, email=email, password=raw_password)
                auth_login(request, user)
                return redirect('home')

        # Only show the landing page with the
        # sign up form
        else:
            form = UserCreationForm()
        return render(request, 'signup.html', {'form': form})

    # If user is authenticated
    # get their timeline/feed
    timeline = get_timeline(request.user)

    return render(request, 'home.html', {"timeline": timeline})


def login(request):
    if request.user.is_authenticated:
        return redirect('home')
    return render(request, 'login.html')


def search(request):
    if not api_key_is_updated():
        return redirect(expired_api_key)

    summoners = []
    if 'nickname' in request.GET:
        nickname = request.GET['nickname']

        found_summoners = Summoner.objects.filter(name__iexact=nickname)

        region_list = ["na1", "br1", "kr", "ru", "oc1", "jp1", "eun1", "euw1", "tr1", "la1", "la2"]

        found_regions = []
        for summoner in found_summoners:
            found_regions.append(summoner.region)
            summoners.append(summoner)

        for region in region_list:
            if region not in found_regions:
                summoner = get_summoner(region, nickname)
                summoners.append(summoner)

    return render(request, 'search.html', {"summoners": summoners})


def summoner(request, region, nickname):
    if not api_key_is_updated():
        return redirect(expired_api_key)

    summoner = get_summoner(region, nickname)

    # If no summoner was found, redirects to the home page
    # (later I will create a customized 'no summoners found' page)
    if summoner == None:
        return redirect("home")

    summoner.leagues = get_leagues(summoner)

    recent_matches = get_recent_matches(summoner)

    is_following = user_is_following(request, summoner)

    return render(request, 'summoner.html',
                  {"summoner": summoner, "recent_matches": recent_matches, "is_following": is_following})


def champions(request):
    latest_version = get_latest_static_data_version()

    jsonresponse = requests.get(
        "http://ddragon.leagueoflegends.com/cdn/" + latest_version + "/data/en_US/champion.json").json()

    # Saving champions data to database
    if "data" in jsonresponse:

        Champion.objects.all().delete()

        for champion, value in jsonresponse["data"].items():
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


@login_required
def following(request):
    user = request.user
    following_list = Following.objects.filter(user=user)

    return render(request, 'following.html', {"following_list": following_list})


def expired_api_key(request):
    return render(request, 'expired_api_key.html')
