from django import forms
from .models import Video
#how to make a form to show on the webpage
class VideoForm(forms.ModelForm):
    class Meta: 
        model = Video
        fields = ['name', 'url','notes']
        #fields have to match the name of the model components
        #go to views.py for further details
class SearchForm(forms.Form):
    search_term = forms.CharField()
