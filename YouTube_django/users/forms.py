from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email','password1', 'password2']



class ProfileUpdate(forms.ModelForm):
	
	class Meta:
		model = Profile
		fields = ['first_name','second_name']


