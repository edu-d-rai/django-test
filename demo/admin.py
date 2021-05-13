from django.contrib import admin

from .models import Album, Concert, Musician, Song

admin.site.register(Musician)
admin.site.register(Album)
admin.site.register(Song)
admin.site.register(Concert)
