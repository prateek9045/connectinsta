from django.contrib import admin

from .models import Trainer, Event, Webinar, Article, Elearning, Olocation, Client, Eventcomment, Eventreview, Clientquery, Webinarreview, Webinarcomment, Olocationcomment, Olocationreview, Elearningcomment, Elearningreview

admin.site.register(Trainer)
admin.site.register(Client)
admin.site.register(Event)
admin.site.register(Webinar)
admin.site.register(Article)
admin.site.register(Elearning)
admin.site.register(Olocation)
admin.site.register(Eventcomment)
admin.site.register(Eventreview)
admin.site.register(Clientquery)
admin.site.register(Webinarcomment)
admin.site.register(Webinarreview)
admin.site.register(Olocationcomment)
admin.site.register(Olocationreview)
admin.site.register(Elearningcomment)
admin.site.register(Elearningreview)
