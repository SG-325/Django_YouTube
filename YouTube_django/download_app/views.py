from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import NewMP3
from django.conf import settings
from pytube import YouTube
import youtube_dl
import os
import requests
import json

# Create your views here.
videos = []


def home(request):
    global videos
    videos.clear()
    
    if request.method == 'POST':
        search_url = 'https://www.googleapis.com/youtube/v3/search'

        search_params = {
            'part':'snippet',
            'q':request.POST['name'],
            'key':settings.YOUTUBE_DATA_API_KEY,
            'type':'video',
            'maxResults':39,
        }
        
        response = requests.get(search_url, params=search_params)
        results = response.json()['items']

        for result in results:
            video_data = {
                'title':result['snippet']['title'],
                'id':result['id']['videoId'],
                'url':F"https://www.youtube.com/watch?v={result['id']['videoId']}",
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
    s = ['"', "'", "&", ";", ":"]
   
    for i in range(len(title_str)):
        if title_str[i] in s:
            video['title'] = f"Audio"
            break

    filename = f"{video['title']}.mp3"

    options = {
        'format': 'bestaudio/best',
        # 'nocheckcertificate' : True,
        'outtmpl': filename,
        'postprocessors': [{
            'key':'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192'
            }]
        }

    if os.path.exists('download_app'):
        os.chdir('download_app/static/download_app/songs')

    with youtube_dl.YoutubeDL(options) as ydl:
        ydl.download([video['url']])
  
    return render(request,'download_app/video_view.html', {'video':video})

