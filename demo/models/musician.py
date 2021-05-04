import uuid
from django.core.validators import MinValueValidator
from django.db import models

class Musician(models.Model) :
    GUITAR = 1
    PIANO = 2
    DRUMS = 3
    BASS = 4
    VOICE = 5
    INSTRUMENT_CHOICES = [
        (GUITAR, 'GUITAR'),
        (PIANO, 'PIANO'),
        (DRUMS, 'DRUMS'),
        (BASS, 'BASS'),
        (VOICE, 'VOICE')
    ]

    influencer = models.ForeignKey('Musician', on_delete=models.SET_NULL, related_name='influenced_musicians', null=True, blank=True)
    preferred_song = models.ForeignKey('Song', on_delete=models.SET_NULL, related_name='song_musician_fans', null=True, blank=True)
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    first_name = models.CharField(max_length=70, null=True, blank=True)
    last_name = models.CharField(max_length=40, null=True, blank=True)
    instrument = models.IntegerField(choices=INSTRUMENT_CHOICES, null=True, blank=True)
    age = models.IntegerField(validators=[MinValueValidator(0)], null=True, blank=True)
    fans = models.BigIntegerField(validators=[MinValueValidator(0)], null=True, blank=True)
    inspired_at = models.TimeField(null=True, blank=True)

