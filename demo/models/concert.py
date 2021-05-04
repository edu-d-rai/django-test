from django.db import models
from django.utils import timezone

class Concert(models.Model) :

    main_artist = models.ForeignKey('Musician', on_delete=models.CASCADE, related_name='main_concerts')
    secondary_artist = models.ForeignKey('Musician', on_delete=models.SET_NULL, related_name='secondary_concerts', null=True, blank=True)
    name = models.CharField(max_length=50, primary_key=True)
    place = models.CharField(max_length=200)
    date = models.DateTimeField(default=timezone.now)
    is_free = models.BooleanField(null=True, blank=True)

