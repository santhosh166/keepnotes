from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from django.forms.models import ModelForm
from .models import content

class registerform(UserCreationForm):
    email=forms.EmailField(required=True)

    class Meta:
        model=User
        fields=['username','email','password1','password2']

class loginform(UserCreationForm):

    class Meta:
        model=User
        fields=['username','password1']

class createform(ModelForm):

    class Meta:
        model=content
        fields=['title','description']