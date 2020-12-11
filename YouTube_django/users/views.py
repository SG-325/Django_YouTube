from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, ProfileUpdate
from download_app.models import NewMP3
from django.contrib import messages
from .models import Profile
import os


# Create your views here.

def user_register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(request,username=username,password=password)

            if not user is None:
                login(request,user)

            messages.add_message(request, messages.SUCCESS, "User created successfully")

            return redirect("login")
        else:
            messages.add_message(request, messages.SUCCESS, "Failed to create user. Please try again")


    form = UserRegisterForm()
    return render(request, 'registration/user_register.html', {'form': form})


@login_required(login_url="login")
def user_profile(request):
    profile = Profile.objects.get(user=request.user)
    videos = NewMP3.objects.all().filter(user=request.user)
    
    list_video = []
    
    for video_1 in videos:    
        count = 0
        k = True

        for i in list_video:
            if video_1.url == i.url:
                k = False
        if k:
            list_video.append(video_1)

        for video_2 in videos:
            if video_1.url == video_2.url:
                count += 1

        video_1.count = count

    return render(request, 'registration/user_profile.html', {"profile":profile, "videos":list_video})


def profile_update(request):
    profile = Profile.objects.get(user=request.user)
    form = ProfileUpdate(instance=profile)

    if request.method == "POST":
        form = ProfileUpdate(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, "User profile updated.")                    

        return redirect('user_profile')

    return render(request, 'registration/user_profile_update.html', {'form': form})

