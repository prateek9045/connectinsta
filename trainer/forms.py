from django import forms
from django.contrib.auth.models import User

from django.forms.widgets import DateTimeInput
from django_countries.widgets import CountrySelectWidget

from .models import *

from .models import Trainer, Event, Webinar, Article, Elearning, Olocation


class TrainerForm(forms.ModelForm):

    class Meta:
        model = Trainer
        fields = ['name', 'mobile', 'organisation', 'designation', 'category', 'picture', 'country']
        widgets = {'country': CountrySelectWidget()}



class ClientForm(forms.ModelForm):

    class Meta:
        model = Client
        fields = ['cname', 'cmobile', 'corganisation', 'cdesignation', 'ccategory', 'cpicture', 'country']
        widgets = {'country': CountrySelectWidget()}


class EventForm(forms.ModelForm):

    class Meta:
        model = Event

        fields = ['etitle', 'ecategory', 'esubcategory', 'eduration', 'edelivery', 'eventstart', 'eventend', 'edescription', 'ecost', 'elocation', 'efacebook', 'ewebsite', 'epicture']
        widgets = {
                    'eventstart': DateTimeInput(attrs={'format': '%Y-%m-%d %H:%M:%S','value':'yyyy-mm-dd hh:mm:ss'}),
                    'eventend': DateTimeInput(attrs={'format': '%Y-%m-%d %H:%M:%S','value':'yyyy-mm-dd hh:mm:ss'}),
        }

class WebinarForm(forms.ModelForm):

    class Meta:
        model = Webinar

        fields = ['wtitle', 'wcategory', 'webinarstart', 'webinarend', 'wdescription', 'wcost', 'wwebsite', 'wpicture']
        widgets = {
            'webinarstart': DateTimeInput(attrs={'format': '%Y-%m-%d %H:%M:%S','value':'yyyy-mm-dd hh:mm:ss'}),
            'webinarend': DateTimeInput(attrs={'format': '%Y-%m-%d %H:%M:%S','value':'yyyy-mm-dd hh:mm:ss'}),
        }



class ArticleForm(forms.ModelForm):

    class Meta:
        model = Article

        fields = ['atitle', 'adiscription', 'acategory', 'apicture']



class ElearningForm(forms.ModelForm):

    class Meta:
        model = Elearning

        fields = ['ltitle', 'ldiscription', 'lcategory', 'lpicture', 'lwebsite']




class OlocationForm(forms.ModelForm):

    class Meta:
        model = Olocation

        fields = ['otitle', 'odiscription', 'location', 'owebsite', 'opicture']



class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)


    class Meta:
        model = User
        fields = ['username', 'email', 'password']



