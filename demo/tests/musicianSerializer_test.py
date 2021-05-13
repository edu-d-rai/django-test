import factory
from datetime import datetime
from django.test import TestCase
from django.urls import reverse
from rest_framework import serializers
from rest_framework.test import APIRequestFactory
from .factories import MusicianFactory, MusicianWithForeignFactory, AlbumFactory, ConcertFactory, SongFactory
from demo.serializers import MusicianSerializer

class MusicianSerializer_Test(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.musician = MusicianWithForeignFactory.create()

    def test_that_a_musician_is_correctly_serialized(self):
        musician = self.musician
        serializer = MusicianSerializer
        serialized_musician = serializer(musician).data

        assert serialized_musician['first_name'] == musician.first_name
        assert serialized_musician['last_name'] == musician.last_name
        assert serialized_musician['instrument'] == musician.instrument
        assert serialized_musician['age'] == musician.age
        assert serialized_musician['fans'] == musician.fans
        assert serialized_musician['inspired_at'] == musician.inspired_at
        assert serialized_musician['id'] == str(musician.id)

        assert len(serialized_musician['prod_records']) == musician.prod_records.count()

        assert len(serialized_musician['main_concerts']) == musician.main_concerts.count()

        assert len(serialized_musician['secondary_concerts']) == musician.secondary_concerts.count()

        assert len(serialized_musician['influenced_musicians']) == musician.influenced_musicians.count()

        assert len(serialized_musician['composed_songs']) == musician.composed_songs.count()

