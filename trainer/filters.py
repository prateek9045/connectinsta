from django.contrib.auth.models import User
from .models import Trainer, Event, Webinar, Elearning, Olocation, Client
import django_filters
from django.forms.widgets import DateTimeInput
from django_countries.widgets import CountrySelectWidget

class UserFilter(django_filters.FilterSet):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email' ]


class EventFilter(django_filters.FilterSet):
    class Meta:
        model = Event
        fields = ['etitle', 'ecategory', 'esubcategory', 'eduration', 'edelivery', 'elocation']



class TrainerFilter(django_filters.FilterSet):
    class Meta:
        model = Trainer
        fields = ['name', 'mobile', 'organisation', 'designation', 'category', 'country']
        widgets = {'country': CountrySelectWidget()}



class WebinarFilter(django_filters.FilterSet):
    class Meta:
        model = Webinar
        fields = ['wtitle', 'wcategory']



class ElearningFilter(django_filters.FilterSet):
    class Meta:
        model = Elearning
        fields = ['ltitle', 'lcategory']


class OlocationFilter(django_filters.FilterSet):
    class Meta:
        model = Olocation
        fields = ['otitle', 'location']