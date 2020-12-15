from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import NewMP3
from django.conf import settings
from isodate import parse_duration
from django.contrib import messages
from pytube import YouTube
import youtube_dl
import os
import time
import requests
import json

# Create your views here.
videos = []


def home(request):
    global videos
    videos.clear()

    if os.path.exists('media'):
        os.chdir('media/songs')

    while os.listdir():
      file = f"{os.getcwd()}/{os.listdir()[0]}"
      os.remove(file)

    
    if request.method == 'POST':
        search_url = 'https://www.googleapis.com/youtube/v3/search'
        video_url = 'https://www.googleapis.com/youtube/v3/videos'

        if request.POST['name'][:8] == "https://":
            search_params = {
                'part':'snippet',
                'q':request.POST['name'],
                'key':settings.YOUTUBE_DATA_API_KEY,
                'type':'video',
                'maxResults':1,
            }
            
        else:
            search_params = {
                'part':'snippet',
                'q':request.POST['name'],
                'key':settings.YOUTUBE_DATA_API_KEY,
                'type':'video',
                'maxResults':39,
            }
            
        response = requests.get(search_url, params=search_params)
        
        results = response.json()['items']


        video_ids = []

        for result in results:
            video_ids.append(result['id']['videoId'])



        video_params = {
            'part':'snippet,contentDetails',
            'key':settings.YOUTUBE_DATA_API_KEY,
            'id':','.join(video_ids)
        }

        response = requests.get(video_url, params=video_params)
        
        results = response.json()['items']


        for result in results:
            video_data = {
                'title':result['snippet']['title'],
                'id':result['id'],
                'url':F"https://www.youtube.com/watch?v={result['id']}",
                'duration':parse_duration(result['contentDetails']['duration']).total_seconds(),
                'thumbnail':result['snippet']['thumbnails']['high']['url'],
            }
            videos.append(video_data)

   
        
    return render(request,'download_app/index.html', {'videos':videos})
    




@login_required(login_url = "login")
def view_video(request, pk):
    global videos

    for v in videos:
        if v['id'] == pk:
            video = v
            break


    video_obj = NewMP3.objects.create(name=video['title'], url=video['url'], user=request.user)

    title_str = video['title']
    s = ['"', "'", "&", ";", ":", " ", "-", "|"]
   
    for i in s:
        while True:
            index = title_str.find(i)
            if index == -1:
                break
            else:
                title_str = title_str[:index] +"_" + title_str[index+1:]
    
    video['title'] = title_str

    filename = f"{video['title']}.mp3"

    options = {
        'format': 'bestaudio/best',
        'nocheckcertificate' : True,
        'outtmpl': filename,
        'postprocessors': [{
            'key':'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192'
            }]
        }

    if os.path.exists('media'):
        os.chdir('media/songs')

    with youtube_dl.YoutubeDL(options) as ydl:
        ydl.download([video['url']])

    if request.POST.get('submit', False) == 'cut':

        start_time = request.POST['time_start']
        end_time = request.POST['time_end']
        
        if start_time == "":
            start_time = "00:00:00"
        
        if end_time == "":
            end_time = video['duration']

        messages.add_message(request, messages.SUCCESS, "The song was split successfully.")
        os.system(f"ffmpeg -i {video['title']}.mp3 -ss {start_time} -t {end_time} {video['title']}_cut.mp3")
        os.remove(f"{video['title']}.mp3")
        os.rename(f"{video['title']}_cut.mp3", f"{video['title']}.mp3")


    return render(request,'download_app/video_view.html', {'video':video})

