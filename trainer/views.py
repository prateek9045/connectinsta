from __future__ import unicode_literals
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.generic import DetailView, TemplateView
from hitcount.views import HitCountDetailView
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.shortcuts import render, render_to_response
from django.views.decorators.csrf import requires_csrf_token
from django.http import HttpResponse,HttpResponseRedirect
from django.template.loader import get_template
from django.template import Context, Template,RequestContext
from django.template.loader import render_to_string
import datetime
import hashlib
from random import randint
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.views.decorators import csrf
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .filters import UserFilter, EventFilter, TrainerFilter, WebinarFilter, ElearningFilter, OlocationFilter
from django.views.generic.edit import UpdateView
from django.core.urlresolvers import reverse_lazy
from .forms import TrainerForm, EventForm, WebinarForm, ArticleForm, UserForm, ElearningForm, OlocationForm, ClientForm
from .models import Trainer, Event, Webinar, Article, Elearning, Olocation, Client, Eventreview, Eventcomment, Clientquery, Webinarcomment, Webinarreview, Olocationreview, Olocationcomment, Elearningreview, Elearningcomment


IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg']


def create_trainer(request):
    if not request.user.is_authenticated():
        return render(request, 'account/login.html')
    else:
        form = TrainerForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            trainer = form.save(commit=False)
            trainer.user = request.user
            trainer.picture = request.FILES['picture']
            file_type = trainer.picture.url.split('.')[-1]
            file_type = file_type.lower()
            if file_type not in IMAGE_FILE_TYPES:
                context = {
                    'trainer': trainer,
                    'form': form,
                    'error_message': 'Image file must be PNG, JPG, or JPEG',
                }
                return render(request, 'trainer/create_trainer.html', context)
            trainer.save()
            return render(request, 'trainer/details.html', {'trainer': trainer})
        context = {
            'form': form,
        }
        return render(request, 'trainer/create_trainer.html', context)




def create_client(request):
    if not request.user.is_authenticated():
        return render(request, 'account/login.html')
    else:
        form = ClientForm(request.POST or None, request.FILES or None)
        if form.is_valid():

            client = form.save(commit=False)
            client.user = request.user
            client.cpicture = request.FILES['cpicture']
            file_type = client.cpicture.url.split('.')[-1]
            file_type = file_type.lower()
            if file_type not in IMAGE_FILE_TYPES:

                context = {
                    'client': client,
                    'form': form,
                    'error_message': 'Image file must be PNG, JPG, or JPEG',
                }

                return render(request, 'trainer/create_client.html', context)
            client.save()
            return render(request, 'trainer/client_details.html', {'client': client})
        context = {
            'form': form,
        }
        return render(request, 'trainer/create_client.html', context)




def create_event(request, trainer_id):
    form = EventForm(request.POST or None, request.FILES or None)
    trainer = get_object_or_404(Trainer, pk=trainer_id)
    event_email = request.user.email
    if form.is_valid():
        trainers_events = trainer.event_set.all()
        for s in trainers_events:
            if s.etitle == form.cleaned_data.get("etitle"):
                context = {
                    'trainer': trainer,
                    'form': form,
                    'error_message': 'You already added that event',
                }
                return render(request, 'trainer/create_event.html', context)
        event = form.save(commit=False)
        event.trainer = trainer
        event.epicture = request.FILES['epicture']
        file_type = event.epicture.url.split('.')[-1]
        file_type = file_type.lower()
        if file_type not in IMAGE_FILE_TYPES:
            context = {
                'trainer': trainer,
                'form': form,
                'error_message': 'Image file must be PNG, JPG, or JPEG',
            }
            return render(request, 'trainer/create_event.html', context)

        event.save()
        send_mail('Connectinsta - New Event Created', 'congratulations', 'prateek@connectinsta.com', [event_email], fail_silently=False)
        return render(request, 'trainer/details.html', {'trainer': trainer})
    context = {
        'trainer': trainer,
        'form': form,
    }
    return render(request, 'trainer/create_event.html', context)





def create_webinar(request, trainer_id):
    form = WebinarForm(request.POST or None, request.FILES or None)
    trainer = get_object_or_404(Trainer, pk=trainer_id)
    webinar_email = request.user.email
    if form.is_valid():
        trainers_webinars = trainer.webinar_set.all()
        for s in trainers_webinars:
            if s.wtitle == form.cleaned_data.get("wtitle"):
                context = {
                    'trainer': trainer,
                    'form': form,
                    'error_message': 'You already added that webinar',
                }
                return render(request, 'trainer/create_webinar.html', context)
        webinar = form.save(commit=False)
        webinar.trainer = trainer
        webinar.wpicture = request.FILES['wpicture']
        file_type = webinar.wpicture.url.split('.')[-1]
        file_type = file_type.lower()
        if file_type not in IMAGE_FILE_TYPES:
            context = {
                'trainer': trainer,
                'form': form,
                'error_message': 'Image file must be PNG, JPG, or JPEG',
            }
            return render(request, 'trainer/create_webinar.html', context)

        webinar.save()
        send_mail('Connectinsta - New Webinar Created', 'congratulations', 'prateek@connectinsta.com', [webinar_email], fail_silently=False)
        return render(request, 'trainer/details.html', {'trainer': trainer})
    context = {
        'trainer': trainer,
        'form': form,
    }
    return render(request, 'trainer/create_webinar.html', context)




def create_article(request, trainer_id):
    form = ArticleForm(request.POST or None, request.FILES or None)
    trainer = get_object_or_404(Trainer, pk=trainer_id)
    article_email = request.user.email
    if form.is_valid():
        trainers_articles = trainer.article_set.all()
        for s in trainers_articles:
            if s.atitle == form.cleaned_data.get("atitle"):
                context = {
                    'trainer': trainer,
                    'form': form,
                    'error_message': 'You already added that article',
                }
                return render(request, 'trainer/create_article.html', context)
        article = form.save(commit=False)
        article.trainer = trainer
        article.epicture = request.FILES['apicture']
        file_type = article.apicture.url.split('.')[-1]
        file_type = file_type.lower()
        if file_type not in IMAGE_FILE_TYPES:
            context = {
                'trainer': trainer,
                'form': form,
                'error_message': 'Image file must be PNG, JPG, or JPEG',
            }
            return render(request, 'trainer/create_article.html', context)

        article.save()
        send_mail('Connectinsta - New Article Created', 'congratulations', 'prateek@connectinsta.com', [article_email], fail_silently=False)
        return render(request, 'trainer/details.html', {'trainer': trainer})
    context = {
        'trainer': trainer,
        'form': form,
    }
    return render(request, 'trainer/create_article.html', context)





def create_elearning(request, trainer_id):
    form = ElearningForm(request.POST or None, request.FILES or None)
    trainer = get_object_or_404(Trainer, pk=trainer_id)
    elearning_email = request.user.email
    if form.is_valid():
        trainers_elearnings = trainer.elearning_set.all()
        for s in trainers_elearnings:
            if s.ltitle == form.cleaned_data.get("ltitle"):
                context = {
                    'trainer': trainer,
                    'form': form,
                    'error_message': 'You already added that Elearning',
                }
                return render(request, 'trainer/create_elearning.html', context)
        elearning = form.save(commit=False)
        elearning.trainer = trainer
        elearning.lpicture = request.FILES['lpicture']
        file_type = elearning.lpicture.url.split('.')[-1]
        file_type = file_type.lower()
        if file_type not in IMAGE_FILE_TYPES:
            context = {
                'trainer': trainer,
                'form': form,
                'error_message': 'Image file must be PNG, JPG, or JPEG',
            }
            return render(request, 'trainer/create_elearning.html', context)

        elearning.save()
        send_mail('Connectinsta - New Elearning Program Created', 'congratulations', 'prateek@connectinsta.com', [elearning_email], fail_silently=False)
        return render(request, 'trainer/details.html', {'trainer': trainer})
    context = {
        'trainer': trainer,
        'form': form,
    }
    return render(request, 'trainer/create_elearning.html', context)




def create_olocation(request, trainer_id):
    form = OlocationForm(request.POST or None, request.FILES or None)
    trainer = get_object_or_404(Trainer, pk=trainer_id)
    olocation_email = request.user.email
    if form.is_valid():
        trainers_olocations = trainer.olocation_set.all()
        for s in trainers_olocations:
            if s.otitle == form.cleaned_data.get("otitle"):
                context = {
                    'trainer': trainer,
                    'form': form,
                    'error_message': 'You already added that Outbound Location',
                }
                return render(request, 'trainer/create_olocation.html', context)
        olocation = form.save(commit=False)
        olocation.trainer = trainer
        olocation.opicture = request.FILES['opicture']
        file_type = olocation.opicture.url.split('.')[-1]
        file_type = file_type.lower()
        if file_type not in IMAGE_FILE_TYPES:
            context = {
                'trainer': trainer,
                'form': form,
                'error_message': 'Image file must be PNG, JPG, or JPEG',
            }
            return render(request, 'trainer/create_olocation.html', context)

        olocation.save()
        send_mail('Connectinsta - New Outbound Location Created', 'congratulations', 'prateek@connectinsta.com', [olocation_email], fail_silently=False)
        return render(request, 'trainer/details.html', {'trainer': trainer})
    context = {
        'trainer': trainer,
        'form': form,
    }
    return render(request, 'trainer/create_olocation.html', context)

def delete_trainer(request, trainer_id):
    trainer = Trainer.objects.get(pk=trainer_id)
    trainer.delete()
    trainers = Trainer.objects.filter(user=request.user)
    return render(request, 'trainer/index.html', {'trainers': trainers})




def delete_client(request, client_id):
    client = Client.objects.get(pk=client_id)
    client.delete()
    clients = Client.objects.filter(user=request.user)
    return render(request, 'trainer/index.html', {'clients': clients})




def delete_event(request, trainer_id, event_id):
    trainer = get_object_or_404(Trainer, pk=trainer_id)
    event = Event.objects.get(pk=event_id)
    event.delete()
    return render(request, 'trainer/details.html', {'trainer': trainer})


def delete_webinar(request, trainer_id, webinar_id):
    trainer = get_object_or_404(Trainer, pk=trainer_id)
    webinar = Webinar.objects.get(pk=webinar_id)
    webinar.delete()
    return render(request, 'trainer/details.html', {'trainer': trainer})



def delete_article(request, trainer_id, article_id):
    trainer = get_object_or_404(Trainer, pk=trainer_id)
    article = Article.objects.get(pk=article_id)
    article.delete()
    return render(request, 'trainer/details.html', {'trainer': trainer})





def delete_elearning(request, trainer_id, elearning_id):
    trainer = get_object_or_404(Trainer, pk=trainer_id)
    elearning = Elearning.objects.get(pk=elearning_id)
    elearning.delete()
    return render(request, 'trainer/details.html', {'trainer': trainer})




def delete_olocation(request, trainer_id, olocation_id):
    trainer = get_object_or_404(Trainer, pk=trainer_id)
    olocation = Olocation.objects.get(pk=olocation_id)
    olocation.delete()
    return render(request, 'trainer/details.html', {'trainer': trainer})




def details(request, trainer_id):
    if not request.user.is_authenticated():
        return render(request, 'account/login.html')
    else:
        user = request.user
        trainer = get_object_or_404(Trainer, pk=trainer_id)
        return render(request, 'trainer/details.html', {'trainer': trainer, 'user': user})


def client_details(request, client_id):
    if not request.user.is_authenticated():
        return render(request, 'account/login.html')
    else:
        user = request.user
        client = get_object_or_404(Client, pk=client_id)
        return render(request, 'trainer/client_details.html', {'client': client, 'user': user})



def edetails(request, trainer_id, event_id):
    if not request.user.is_authenticated():
        return render(request, 'account/login.html')
    else:
        user = request.user
        trainer = get_object_or_404(Trainer, pk=trainer_id)
        event = Event.objects.get(pk=event_id)
        return render(request, 'trainer/event_details.html', {'event': event, 'trainer':trainer, 'user': user})



def wdetails(request, trainer_id, webinar_id):
    if not request.user.is_authenticated():
        return render(request, 'account/login.html')
    else:
        user = request.user
        trainer = get_object_or_404(Trainer, pk=trainer_id)
        webinar = Webinar.objects.get(pk=webinar_id)
        return render(request, 'trainer/webinar_details.html', {'webinar': webinar, 'trainer':trainer, 'user': user})




def adetails(request, trainer_id, article_id):
    if not request.user.is_authenticated():
        return render(request, 'account/login.html')
    else:
        user = request.user
        trainer = get_object_or_404(Trainer, pk=trainer_id)
        article = Article.objects.get(pk=article_id)
        return render(request, 'trainer/article_details.html', {'article': article, 'trainer':trainer, 'user': user})



def ldetails(request, trainer_id, elearning_id):
    if not request.user.is_authenticated():
        return render(request, 'account/login.html')
    else:
        user = request.user
        trainer = get_object_or_404(Trainer, pk=trainer_id)
        elearning = Elearning.objects.get(pk=elearning_id)
        return render(request, 'trainer/elearning_details.html', {'elearning': elearning, 'trainer':trainer, 'user': user})



def odetails(request, trainer_id, olocation_id):
    if not request.user.is_authenticated():
        return render(request, 'account/login.html')
    else:
        user = request.user
        trainer = get_object_or_404(Trainer, pk=trainer_id)
        olocation = Olocation.objects.get(pk=olocation_id)
        return render(request, 'trainer/olocation_details.html', {'olocation': olocation, 'trainer':trainer, 'user': user})



def favorite(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    try:
        if event.is_favorite:
            event.is_favorite = False
        else:
            event.is_favorite = True
        event.save()
    except (KeyError, Event.DoesNotExist):
        return JsonResponse({'success': False})
    else:
        return JsonResponse({'success': True})



def favorite_webinar(request, webinar_id):
    webinar = get_object_or_404(Webinar, pk=webinar_id)
    try:
        if webinar.is_favorite:
            webinar.is_favorite = False
        else:
            webinar.is_favorite = True
        webinar.save()
    except (KeyError, Webinar.DoesNotExist):
        return JsonResponse({'success': False})
    else:
        return JsonResponse({'success': True})



def favorite_article(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    try:
        if article.is_favorite:
            article.is_favorite = False
        else:
            article.is_favorite = True
        article.save()
    except (KeyError, Article.DoesNotExist):
        return JsonResponse({'success': False})
    else:
        return JsonResponse({'success': True})





def favorite_elearning(request, elearning_id):
    elearning = get_object_or_404(Elearning, pk=elearning_id)
    try:
        if elearning.is_favorite:
            elearning.is_favorite = False
        else:
            elearning.is_favorite = True
        elearning.save()
    except (KeyError, Elearning.DoesNotExist):
        return JsonResponse({'success': False})
    else:
        return JsonResponse({'success': True})




def favorite_olocation(request, olocation_id):
    olocation = get_object_or_404(Olocation, pk=olocation_id)
    try:
        if olocation.is_favorite:
            olocation.is_favorite = False
        else:
            olocation.is_favorite = True
        olocation.save()
    except (KeyError, Olocation.DoesNotExist):
        return JsonResponse({'success': False})
    else:
        return JsonResponse({'success': True})





def favorite_trainer(request, trainer_id):
    trainer = get_object_or_404(Trainer, pk=trainer_id)
    try:
        if trainer.is_favorite:
            trainer.is_favorite = False
        else:
            trainer.is_favorite = True
            trainer.save()
    except (KeyError, Trainer.DoesNotExist):
        return JsonResponse({'success': False})
    else:
        return JsonResponse({'success': True})







def index(request):
    if not request.user.is_authenticated():
        return render(request, 'account/login.html')
    else:
        trainers = Trainer.objects.filter(user=request.user)
        clients = Client.objects.filter(user=request.user)
        event_results = Event.objects.all()
        query = request.GET.get("q")
        if query:
            trainers = trainers.filter(
                Q(name__icontains=query) |
                Q(designation__icontains=query)
            ).distinct()
            event_results = event_results.filter(
                Q(etitle__icontains=query)
            ).distinct()
            return render(request, 'trainer/index.html', {
                'trainers': trainers,
                'events': event_results,
                'clients': clients,
            })
        else:
            return render(request, 'trainer/index.html', {'trainers': trainers, 'clients': clients})





def logout_user(request):
    logout(request)
    form = UserForm(request.POST or None)
    context = {
        "form": form,
    }
    return render(request, 'account/login.html', context)






def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                trainers = Trainer.objects.filter(user=request.user)
                return render(request, 'trainer/index.html', {'trainers': trainers})
            else:
                return render(request, 'account/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'account/login.html', {'error_message': 'Invalid login'})
    return render(request, 'account/login.html')





def register(request):
    form = UserForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                trainers = Trainer.objects.filter(user=request.user)
                return render(request, 'account/login.html', {'trainers': trainers})
    context = {
        "form": form,
    }
    return render(request, 'account/signup.html', context)





def events(request, filter_by):
    if not request.user.is_authenticated():
        return render(request, 'account/login.html')
    else:
        try:
            event_ids = []
            for trainer in Trainer.objects.filter(user=request.user):
                for event in trainer.event_set.all():
                    event_ids.append(event.pk)
            users_events = Event.objects.filter(pk__in=event_ids)
            if filter_by == 'favorite':
                users_events = users_events.filter(is_favorite=True)
        except Trainer.DoesNotExist:
            users_events = []
        return render(request, 'trainer/events.html', {
            'event_list': users_events,
            'filter_by': filter_by,
        })





def webinars(request, filter_by):
    if not request.user.is_authenticated():
        return render(request, 'account/login.html')
    else:
        try:
            webinar_ids = []
            for trainer in Trainer.objects.filter(user=request.user):
                for webinar in trainer.webinar_set.all():
                    webinar_ids.append(webinar.pk)
            users_webinars = Webinar.objects.filter(pk__in=webinar_ids)
            if filter_by == 'favorite_webinar':
                users_webinars = users_webinars.filter(is_favorite=True)
        except Trainer.DoesNotExist:
            users_webinars = []
        return render(request, 'trainer/webinars.html', {
            'webinar_list': users_webinars,
            'filter_by': filter_by,
        })






def articles(request, filter_by):
    if not request.user.is_authenticated():
        return render(request, 'account/login.html')
    else:
        try:
            article_ids = []
            for trainer in Trainer.objects.filter(user=request.user):
                for article in trainer.article_set.all():
                    article_ids.append(article.pk)
            users_articles = Article.objects.filter(pk__in=article_ids)
            if filter_by == 'favorite_article':
                users_articles = users_articles.filter(is_favorite=True)
        except Trainer.DoesNotExist:
            users_articles = []
        return render(request, 'trainer/articles.html', {
            'article_list': users_articles,
            'filter_by': filter_by,
        })




def elearnings(request, filter_by):
    if not request.user.is_authenticated():
        return render(request, 'account/login.html')
    else:
        try:
            elearning_ids = []
            for trainer in Trainer.objects.filter(user=request.user):
                for elearning in trainer.elearning_set.all():
                    elearning_ids.append(elearning.pk)
            users_elearnings = Elearning.objects.filter(pk__in=elearning_ids)
            if filter_by == 'favorite_elearning':
                users_elearnings = users_elearnings.filter(is_favorite=True)
        except Trainer.DoesNotExist:
            users_elearnings = []
        return render(request, 'trainer/elearnings.html', {
            'elearning_list': users_elearnings,
            'filter_by': filter_by,
        })





def olocations(request, filter_by):
    if not request.user.is_authenticated():
        return render(request, 'account/login.html')
    else:
        try:
            olocation_ids = []
            for trainer in Trainer.objects.filter(user=request.user):
                for olocation in trainer.olocation_set.all():
                    olocation_ids.append(olocation.pk)
            users_olocations = Olocation.objects.filter(pk__in=olocation_ids)
            if filter_by == 'favorite_olocation':
                users_olocations = users_olocations.filter(is_favorite=True)
        except Trainer.DoesNotExist:
            users_olocations = []
        return render(request, 'trainer/olocations.html', {
            'olocation_list': users_olocations,
            'filter_by': filter_by,
        })




class TrainerUpdate(UpdateView):
    model = Trainer
    success_url = reverse_lazy('trainer:index')
    form_class = TrainerForm



class ClientUpdate(UpdateView):
    model = Client
    success_url = reverse_lazy('trainer:index')
    form_class = ClientForm


class EventUpdate(UpdateView):
    model = Event
    success_url = reverse_lazy('trainer:index')
    form_class = EventForm


class WebinarUpdate(UpdateView):
    model = Webinar
    success_url = reverse_lazy('trainer:index')
    form_class = WebinarForm



class ArticleUpdate(UpdateView):
    model = Article
    success_url = reverse_lazy('trainer:index')
    form_class = ArticleForm



class ElearningUpdate(UpdateView):
    model = Elearning
    success_url = reverse_lazy('trainer:index')
    form_class = ElearningForm




class LocationUpdate(UpdateView):
    model = Olocation
    success_url = reverse_lazy('trainer:index')
    form_class = OlocationForm




def review_details(request, trainer_id, event_id):
    trainer = get_object_or_404(Trainer, pk=trainer_id)
    event = Event.objects.get(pk=event_id)
    review = request.POST.get("review")
    rating = request.POST.get("rating")
    Eventreview.objects.create(review=review,rating=rating,event_id=event_id, trainer_id=trainer_id)
    return render(request, 'trainer/event_details.html', {'trainer': trainer ,'event': event})



def review_comment(request, trainer_id, event_id, eventreview_id):
    trainer = get_object_or_404(Trainer, pk=trainer_id)
    event = Event.objects.get(pk=event_id)
    comment = request.POST.get("comment")
    Eventcomment.objects.create(comment=comment,trainer_id=trainer_id,event_id=event_id,eventreview_id=eventreview_id)
    rev = Eventcomment.objects.filter(eventreview=eventreview_id)
    context = {
        'rev': rev
    }
    return render(request, 'trainer/event_details.html', {'trainer':trainer , 'event':event}, context)



def client_query(request,trainer_id):
    trainer = get_object_or_404(Trainer, pk=trainer_id)
    subject = request.POST.get("subject")
    message = request.POST.get("message")
    Clientquery.objects.create(subject=subject,message=message,trainer_id=trainer_id)
    return render(request, 'trainer/details.html', {'trainer':trainer})



def delete_query(request, trainer_id, eventquery_id):
    trainer = get_object_or_404(Trainer, pk=trainer_id)
    eventquery = Clientquery.objects.get(pk=eventquery_id)
    eventquery.delete()
    return render(request, 'trainer/details.html', {'trainer': trainer})




def review_webinar(request, trainer_id, webinar_id):
    trainer = get_object_or_404(Trainer, pk=trainer_id)
    webinar = Webinar.objects.get(pk=webinar_id)
    review = request.POST.get("review")
    rating = request.POST.get("rating")
    Webinarreview.objects.create(review=review,rating=rating,webinar_id=webinar_id, trainer_id=trainer_id)
    return render(request, 'trainer/webinar_details.html', {'trainer': trainer ,'webinar': webinar})



def comment_webinar(request, trainer_id, webinar_id, webinarreview_id):
    trainer = get_object_or_404(Trainer, pk=trainer_id)
    webinar = Webinar.objects.get(pk=webinar_id)
    comment = request.POST.get("comment")
    Webinarcomment.objects.create(comment=comment,trainer_id=trainer_id,webinar_id=webinar_id,webinarreview_id=webinarreview_id)
    return render(request, 'trainer/webinar_details.html', {'trainer':trainer , 'webinar':webinar})


def review_olocation(request, trainer_id, olocation_id):
    trainer = get_object_or_404(Trainer, pk=trainer_id)
    olocation = Olocation.objects.get(pk=olocation_id)
    review = request.POST.get("review")
    rating = request.POST.get("rating")
    Olocationreview.objects.create(review=review,rating=rating,olocation_id=olocation_id, trainer_id=trainer_id)
    return render(request, 'trainer/olocation_details.html', {'trainer': trainer ,'olocation': olocation})



def comment_olocation(request, trainer_id, olocation_id, olocationreview_id):
    trainer = get_object_or_404(Trainer, pk=trainer_id)
    olocation = Olocation.objects.get(pk=olocation_id)
    comment = request.POST.get("comment")
    Olocationcomment.objects.create(comment=comment,trainer_id=trainer_id,olocation_id=olocation_id,olocationreview_id=olocationreview_id)
    return render(request, 'trainer/olocation_details.html', {'trainer':trainer , 'olocation':olocation})



def review_elearning(request, trainer_id, elearning_id):
    trainer = get_object_or_404(Trainer, pk=trainer_id)
    elearning = Elearning.objects.get(pk=elearning_id)
    review = request.POST.get("review")
    rating = request.POST.get("rating")
    Elearningreview.objects.create(review=review,rating=rating,elearning_id=elearning_id, trainer_id=trainer_id)
    return render(request, 'trainer/elearning_details.html', {'trainer': trainer ,'elearning': elearning})



def comment_elearning(request, trainer_id, elearning_id, elearningreview_id):
    trainer = get_object_or_404(Trainer, pk=trainer_id)
    elearning = Elearning.objects.get(pk=elearning_id)
    comment = request.POST.get("comment")
    Elearningcomment.objects.create(comment=comment,trainer_id=trainer_id,elearning_id=elearning_id,elearningreview_id=elearningreview_id)
    return render(request, 'trainer/elearning_details.html', {'trainer':trainer , 'elearning':elearning})



def search(request):
    user_list = User.objects.all()
    user_filter = UserFilter(request.GET, queryset=user_list)
    return render(request, 'trainer/user_list.html', {'filter': user_filter})


def eventsearch(request):
    event_list = Event.objects.all()
    event_filter = EventFilter(request.GET, queryset=event_list)
    return render(request, 'trainer/event_list.html', {'filter': event_filter})


def trainersearch(request):
    trainer_list = Trainer.objects.all()
    trainer_filter = TrainerFilter(request.GET, queryset=trainer_list)
    return render(request, 'trainer/trainer_list.html', {'filter': trainer_filter})


def webinarsearch(request):
    webinar_list = Webinar.objects.all()
    webinar_filter = WebinarFilter(request.GET, queryset=webinar_list)
    return render(request, 'trainer/webinar_list.html', {'filter': webinar_filter})


def elearningsearch(request):
    elearning_list = Elearning.objects.all()
    elearning_filter = ElearningFilter(request.GET, queryset=elearning_list)
    return render(request, 'trainer/elearning_list.html', {'filter': elearning_filter})


def olocationsearch(request):
    olocation_list = Olocation.objects.all()
    olocation_filter = OlocationFilter(request.GET, queryset=olocation_list)
    return render(request, 'trainer/olocation_list.html', {'filter': olocation_filter})




class TrainerMixinDetailView(object):
    """
    Mixin to same us some typing.  Adds context for us!
    """
    model = Trainer

    def get_context_data(self, **kwargs):
        context = super(TrainerMixinDetailView, self).get_context_data(**kwargs)
        context['trainer_list'] = Trainer.objects.all()[:5]
        context['trainer_views'] = ["ajax", "detail", "detail-with-count"]
        return context




class TrainerDetailJSONView(TrainerMixinDetailView, DetailView):
    template_name = 'trainer/trainer_ajax.html'

    @classmethod
    def as_view(cls, **initkwargs):
        view = super(TrainerDetailJSONView, cls).as_view(**initkwargs)
        return ensure_csrf_cookie(view)


class IndexView(TrainerMixinDetailView, TemplateView):
    template_name = 'trainer/details.html'



class TrainerDetailView(TrainerMixinDetailView, HitCountDetailView):
    """
    Generic hitcount class based view.
    """
    pass


class TrainerCountHitDetailView(TrainerMixinDetailView, HitCountDetailView):
    """
    Generic hitcount class based view that will also perform the hitcount logic.
    """
    count_hit = True



def Home(request):
	MERCHANT_KEY = "uW5swwvR"
	key="uW5swwvR"
	SALT = "TEFmxa9zRV"
	PAYU_BASE_URL = "https://test.payu.in/_payment"
	action = ''
	posted={}
	for i in request.POST:
		posted[i]=request.POST[i]
	hash_object = hashlib.sha256(b'randint(0,20)')
	txnid=hash_object.hexdigest()[0:20]
	hashh = ''
	posted['txnid']=txnid
	hashSequence = "key|txnid|amount|productinfo|firstname|email|udf1|udf2|udf3|udf4|udf5|udf6|udf7|udf8|udf9|udf10"
	posted['key']=key
	hash_string=''
	hashVarsSeq=hashSequence.split('|')
	for i in hashVarsSeq:
		try:
			hash_string+=str(posted[i])
		except Exception:
			hash_string+=''
		hash_string+='|'
	hash_string+=SALT
	hashh=hashlib.sha512(hash_string).hexdigest().lower()
	action =PAYU_BASE_URL
	if(posted.get("key")!=None and posted.get("txnid")!=None and posted.get("productinfo")!=None and posted.get("firstname")!=None and posted.get("email")!=None):

		return render_to_response('trainer/current_datetime.html',context={'posted':posted,'hashh':hashh,'MERCHANT_KEY':MERCHANT_KEY,'txnid':txnid,'hash_string':hash_string,'action':'https://test.payu.in/_payment' })
	else:
		return render_to_response('trainer/current_datetime.html',context={'posted':posted,'hashh':hashh,'MERCHANT_KEY':MERCHANT_KEY,'txnid':txnid,'hash_string':hash_string,'action':'.' })

@csrf_protect
@csrf_exempt
@requires_csrf_token
def success(request):
	c = {}
        c.update(csrf(request))
	status=request.POST["status"]
	firstname=request.POST["firstname"]
	amount=request.POST["amount"]
	txnid=request.POST["txnid"]
	posted_hash=request.POST["hash"]
	key=request.POST["key"]
	productinfo=request.POST["productinfo"]
	email=request.POST["email"]
	salt="TEFmxa9zRV"
	try:
		additionalCharges=request.POST["additionalCharges"]
		retHashSeq=additionalCharges+'|'+salt+'|'+status+'|||||||||||'+email+'|'+firstname+'|'+productinfo+'|'+amount+'|'+txnid+'|'+key
	except Exception:
		retHashSeq = salt+'|'+status+'|||||||||||'+email+'|'+firstname+'|'+productinfo+'|'+amount+'|'+txnid+'|'+key
	hashh=hashlib.sha512(retHashSeq).hexdigest().lower()
	if(hashh !=posted_hash):
		print "Invalid Transaction. Please try again"
	else:
		print "Thank You. Your order status is ", status
		print "Your Transaction ID for this transaction is ",txnid
		print "We have received a payment of Rs. ", amount ,". Your order will soon be shipped."
	return render_to_response('trainer/sucess.html',context={'txnid':txnid,'status':status,'amount':amount})


@csrf_protect
@csrf_exempt
@requires_csrf_token
def failure(request):
	c = {}
    	c.update(csrf(request))
	status=request.POST["status"]
	firstname=request.POST["firstname"]
	amount=request.POST["amount"]
	txnid=request.POST["txnid"]
	posted_hash=request.POST["hash"]
	key=request.POST["key"]
	productinfo=request.POST["productinfo"]
	email=request.POST["email"]
	salt="TEFmxa9zRV"
	try:
		additionalCharges=request.POST["additionalCharges"]
		retHashSeq=additionalCharges+'|'+salt+'|'+status+'|||||||||||'+email+'|'+firstname+'|'+productinfo+'|'+amount+'|'+txnid+'|'+key
	except Exception:
		retHashSeq = salt+'|'+status+'|||||||||||'+email+'|'+firstname+'|'+productinfo+'|'+amount+'|'+txnid+'|'+key
	hashh=hashlib.sha512(retHashSeq).hexdigest().lower()
	if(hashh !=posted_hash):
		print "Invalid Transaction. Please try again"
	else:
		print "Thank You. Your order status is ", status
		print "Your Transaction ID for this transaction is ",txnid
		print "We have received a payment of Rs. ", amount ,". Your order will soon be shipped."
 	return render_to_response("trainer/Failure.html",c)



