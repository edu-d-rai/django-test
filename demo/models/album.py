from datetime import date
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

class Album(models.Model) :
    ROCK = 1
    POP = 2
    FOLK = 3
    GENRE_CHOICES = [
        (ROCK, 'ROCK'),
        (POP, 'POP'),
        (FOLK, 'FOLK')
    ]

    producer = models.ForeignKey('Musician', on_delete=models.SET_NULL, related_name='prod_records', null=True, blank=True)
    interpreters = models.ManyToManyField('Musician', related_name='albums', db_table='records_interpreters', blank=True)
    collaborators = models.ManyToManyField('Musician', related_name='collab_albums', db_table='records_collaborators', blank=True)
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=80, unique=True)
    genre = models.IntegerField(choices=GENRE_CHOICES, null=True, blank=True)
    release_date = models.DateField(null=True, blank=True, default=date.today)
    num_stars = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)], null=True, blank=True)
    ranking = models.FloatField(validators=[MinValueValidator(2.0), MaxValueValidator(10.2)], null=True, blank=True, default=3.0)
    upc = models.CharField(max_length=12, null=True, blank=True)

