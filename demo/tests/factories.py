import factory
from datetime import timezone, timedelta
from factory import LazyFunction, LazyAttribute, SubFactory, fuzzy
from factory.django import DjangoModelFactory
from faker import Factory
from random import randint, uniform

from demo.models import Musician, Album, Song, Concert

faker = Factory.create()

class MusicianFactory(DjangoModelFactory):
    class Meta:
        model = Musician

    first_name = LazyAttribute(lambda o: faker.text(max_nb_chars = 70))
    last_name = LazyAttribute(lambda o: faker.text(max_nb_chars = 40))
    instrument = fuzzy.FuzzyChoice(Musician.INSTRUMENT_CHOICES,getter=lambda c: c[0])
    age = LazyAttribute(lambda o: randint(0, 10000))
    fans = LazyAttribute(lambda o: randint(0, 10000))
    inspired_at = LazyFunction(faker.time)

class MusicianWithForeignFactory(MusicianFactory):
    @factory.post_generation
    def prod_records(obj, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for n in range(extracted):
                AlbumFactory(producer=obj)
        else:
            number_of_units = randint(1, 10)
            for n in range(number_of_units):
                AlbumFactory(producer=obj)
    @factory.post_generation
    def main_concerts(obj, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for n in range(extracted):
                ConcertFactory(main_artist=obj)
        else:
            number_of_units = randint(1, 10)
            for n in range(number_of_units):
                ConcertFactory(main_artist=obj)
    @factory.post_generation
    def secondary_concerts(obj, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for n in range(extracted):
                ConcertFactory(secondary_artist=obj)
        else:
            number_of_units = randint(1, 10)
            for n in range(number_of_units):
                ConcertFactory(secondary_artist=obj)
    @factory.post_generation
    def influenced_musicians(obj, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for n in range(extracted):
                MusicianFactory(influencer=obj)
        else:
            number_of_units = randint(1, 10)
            for n in range(number_of_units):
                MusicianFactory(influencer=obj)
    @factory.post_generation
    def composed_songs(obj, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for n in range(extracted):
                SongFactory(composer=obj)
        else:
            number_of_units = randint(1, 10)
            for n in range(number_of_units):
                SongFactory(composer=obj)

class AlbumFactory(DjangoModelFactory):
    class Meta:
        model = Album

    name = LazyAttribute(lambda o: faker.text(max_nb_chars = 80))
    genre = fuzzy.FuzzyChoice(Album.GENRE_CHOICES,getter=lambda c: c[0])
    release_date = LazyFunction(faker.date)
    num_stars = LazyAttribute(lambda o: randint(0, 5))
    ranking = uniform(2.0, 10.2)
    upc = LazyAttribute(lambda o: faker.text(max_nb_chars = 12))

class AlbumWithForeignFactory(AlbumFactory):
    @factory.post_generation
    def songs(obj, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for n in range(extracted):
                SongFactory(album=obj)
        else:
            number_of_units = randint(1, 10)
            for n in range(number_of_units):
                SongFactory(album=obj)

class SongFactory(DjangoModelFactory):
    class Meta:
        model = Song
        django_get_or_create = ('id',)

    album = factory.SubFactory('demo.tests.factories.AlbumFactory')
    composer = factory.SubFactory('demo.tests.factories.MusicianFactory')
    id = LazyAttribute(lambda o: randint(0, 10000))
    name = LazyAttribute(lambda o: faker.text(max_nb_chars = 100))
    lyrics = LazyAttribute(lambda o: faker.text(max_nb_chars = 1000))

class SongWithForeignFactory(SongFactory):
    @factory.post_generation
    def song_musician_fans(obj, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for n in range(extracted):
                MusicianFactory(preferred_song=obj)
        else:
            number_of_units = randint(1, 10)
            for n in range(number_of_units):
                MusicianFactory(preferred_song=obj)

class ConcertFactory(DjangoModelFactory):
    class Meta:
        model = Concert
        django_get_or_create = ('name',)

    main_artist = factory.SubFactory('demo.tests.factories.MusicianFactory')
    name = LazyAttribute(lambda o: faker.text(max_nb_chars = 50) .replace('.',''))
    place = LazyAttribute(lambda o: faker.text(max_nb_chars = 200))
    date = LazyAttribute(lambda o: faker.date_time(tzinfo = timezone(timedelta(0))).isoformat())
    is_free = LazyFunction(faker.boolean)



