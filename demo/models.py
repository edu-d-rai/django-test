import uuid
from datetime import date

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone


class Musician(models.Model):
    GUITAR = 'GUITAR'
    PIANO = 'PIANO'
    DRUMS = 'DRUMS'
    BASS = 'BASS'
    VOICE = 'VOICE'
    INSTRUMENT_CHOICES = [
        (GUITAR, 'GUITAR'),
        (PIANO, 'PIANO'),
        (DRUMS, 'DRUMS'),
        (BASS, 'BASS'),
        (VOICE, 'VOICE')
    ]

    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    first_name = models.CharField(max_length=70, null=True, blank=True)
    last_name = models.CharField(max_length=40, null=True, blank=True)
    instrument = models.CharField(max_length=6, choices=INSTRUMENT_CHOICES, null=True, blank=True)
    age = models.IntegerField(validators=[MinValueValidator(0)], null=True, blank=True)
    fans = models.BigIntegerField(validators=[MinValueValidator(0)], null=True, blank=True)
    inspired_at = models.TimeField(null=True, blank=True)
    influencer = models.ForeignKey('Musician', on_delete=models.SET_NULL,
                                   related_name='influenced_musicians', null=True, blank=True)
    preferred_song = models.ForeignKey('Song', on_delete=models.SET_NULL,
                                       related_name='song_musician_fans', null=True, blank=True)

    class Meta:
        db_table = "musician"


class Album(models.Model):
    ROCK = 'ROCK'
    POP = 'POP'
    FOLK = 'FOLK'
    GENRE_CHOICES = [
        (ROCK, 'ROCK'),
        (POP, 'POP'),
        (FOLK, 'FOLK')
    ]

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=80, unique=True)
    genre = models.CharField(max_length=4, choices=GENRE_CHOICES, null=True, blank=True)
    release_date = models.DateField(null=True, blank=True, default=date.today)
    num_stars = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)], null=True, blank=True)
    ranking = models.FloatField(validators=[MinValueValidator(
        2.0), MaxValueValidator(10.2)], null=True, blank=True, default=3.0)
    upc = models.CharField(max_length=12, null=True, blank=True)
    producer = models.ForeignKey('Musician', on_delete=models.SET_NULL,
                                 related_name='prod_records', null=True, blank=True)
    interpreters = models.ManyToManyField('Musician', related_name='albums',
                                          db_table='records_interpreters', blank=True)
    collaborators = models.ManyToManyField('Musician', related_name='collab_albums',
                                           db_table='records_collaborators', blank=True)

    class Meta:
        db_table = "album"


class Song(models.Model):

    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    lyrics = models.CharField(max_length=1000, null=True, blank=True)
    code = models.UUIDField(null=True, blank=True, default=uuid.uuid4, editable=False)
    album = models.ForeignKey('Album', on_delete=models.CASCADE, related_name='songs')
    composer = models.ForeignKey('Musician', on_delete=models.CASCADE, related_name='composed_songs')

    class Meta:
        db_table = "song"


class Concert(models.Model):

    name = models.CharField(max_length=50, primary_key=True)
    place = models.CharField(max_length=200)
    date = models.DateTimeField(null=True, blank=True, default=timezone.now)
    is_free = models.BooleanField(null=True, blank=True)
    main_artist = models.ForeignKey('Musician', on_delete=models.CASCADE, related_name='main_concerts')
    secondary_artist = models.ForeignKey('Musician', on_delete=models.SET_NULL,
                                         related_name='secondary_concerts', null=True, blank=True)

    class Meta:
        db_table = "concert"
