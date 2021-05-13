from datetime import datetime

import factory
from django.test import TestCase
from django.urls import reverse
from rest_framework import serializers
from rest_framework.test import APIRequestFactory

from demo.serializers import Musician2Serializer

from .factories import (
    AlbumFactory,
    ConcertFactory,
    MusicianFactory,
    MusicianWithForeignFactory,
    SongFactory,
)


class Musician2Serializer_Test(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.musician = MusicianWithForeignFactory.create()

    def test_that_a_musician_is_correctly_serialized(self):
        musician = self.musician
        serializer = Musician2Serializer
        serialized_musician = serializer(musician).data

        assert serialized_musician['first_name'] == musician.first_name
        assert serialized_musician['last_name'] == musician.last_name
        assert serialized_musician['id'] == str(musician.id)

        assert len(serialized_musician['prod_records']) == musician.prod_records.count()
