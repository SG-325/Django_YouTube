from django import forms
from django.forms import ModelForm
from .models import NewMP3


class MP3Form(ModelForm):
    class Meta:
        model = NewMP3
        fields = '__all__'
        exclude = ['user']
