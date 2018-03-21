import requests
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

from core.forms import SignUpForm


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
            'https://' + region + '.api.riotgames.com/lol/summoner/v3/summoners/by-name/' + nickname + '?api_key=RGAPI-90ab841e-f0e2-4ba4-ae02-f871df546eec')
        summoner = response.json()

    return render(request, 'home.html', {"summoner": summoner})

def login(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        return render(request, 'login.html')