from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
from .models import Image

class ProfileUpdate(forms.ModelForm):
    class Meta:
        model=Profile
        fields=['photo','fname','lname','email']
        widgets = {
            'photo': forms.FileInput(attrs={'class': 'custom-class'}),
            'fname': forms.TextInput(attrs={'size': '20', 'class': 'custom-class'}),
            'lname': forms.TextInput(attrs={'size': '20', 'class': 'custom-class'}),
            'email': forms.EmailInput(attrs={'size': '30', 'class': 'custom-class'}),
        }
        labels = {
            'photo':'Profile Picture',
            'fname': 'First Name',
            'lname':'Last Name',
            'email':'E-mail'
        }

class ImageUploadForm(forms.ModelForm):
    class Meta:
        model=Image
        fields=['image']