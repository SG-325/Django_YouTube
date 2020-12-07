from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import NewMP3
from .forms import MP3Form
from django.contrib import messages
from django.conf import settings
from pytube import YouTube
import youtube_dl
import os
import requests
import json

# Create your views here.
videos = []
video = {}


def home(request):
    global videos
    videos.clear()
    
    if request.method == 'POST':
        search_url = 'https://www.googleapis.com/youtube/v3/search'
        # video_url = 'https://www.googleapis.com/youtube/v3/videos'


        search_params = {
            'part':'snippet',
            'q':request.POST['name'],
            'key':settings.YOUTUBE_DATA_API_KEY,
            'type':'video',
            'maxResults':39,
        }
        
        response = requests.get(search_url, params=search_params)
        # print(response.json())
        results = response.json()['items']

        for result in results:
            video_data = {
                'title':result['snippet']['title'],
                'id':result['id']['videoId'],
                'url':F"https://www.youtube.com/watch?v={result['id']['videoId']}",
                'thumbnail':result['snippet']['thumbnails']['high']['url'],
                'source':F"/static/download_app/songs/{result['snippet']['title']}___{result['id']['videoId']}.mp3"
            }
            videos.append(video_data)
        
    return render(request,'download_app/index.html', {'videos':videos})
    

@login_required(login_url = "login")
def view_video(request, pk):
    global videos
    global video

    for v in videos:
        if v['id'] == pk:
            video = v
            break

    # video_url = video['url']
    # video_info = youtube_dl.YoutubeDL().extract_info(url=video_url)
    # filename = f"{video_info['title']}.mp3"

    # options = {
    #     'format': 'bestaudio/best',
    #     'nocheckcertificate' : True,
    #     # 'keepvideo': False,
    #     'outtmpl': filename,
    #     'postprocessors': [{
    #         'key':'FFmpegExtractAudio',
    #         'preferredcodec': 'mp3',
    #         'preferredquality': '192'
    #         }]
    #     }

    # os.chdir('download_app/static/download_app/songs')

    # with youtube_dl.YoutubeDL(options) as ydl:
    #     ydl.download([video_url])
  
    return render(request,'download_app/video_view.html', {'video':video})



def download(request):
    global video
    video_url = video['url']
    video_obj = NewMP3.objects.create(user=request.user, name=video['title'], url=video['url'])
    # video_info = youtube_dl.YoutubeDL().extract_info(url=video_url)
    # filename = f"{video_info['title']}.mp3"

    options = {
        'format': 'bestaudio/best',
        'nocheckcertificate' : True,
        # 'keepvideo': False,
        # 'outtmpl': filename,
        'postprocessors': [{
            'key':'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192'
            }]
        }

    os.chdir(os.path.expanduser('~') + '/Downloads')
    with youtube_dl.YoutubeDL(options) as ydl:
        ydl.download([video_url])

    return render(request,'download_app/index.html', {'video':video})



