from datetime import datetime

import factory
from django.test import TestCase
from django.urls import reverse
from rest_framework import serializers
from rest_framework.test import APIRequestFactory

from demo.serializers import SongSerializer

from .factories import (
    AlbumFactory,
    MusicianFactory,
    SongFactory,
    SongWithForeignFactory,
)


class SongSerializer_Test(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.song = SongWithForeignFactory.create()

    def test_that_a_song_is_correctly_serialized(self):
        song = self.song
        serializer = SongSerializer
        serialized_song = serializer(song).data

        assert serialized_song['id'] == song.id
        assert serialized_song['name'] == song.name
        assert serialized_song['lyrics'] == song.lyrics
        assert serialized_song['code'] == str(song.code)

        assert len(serialized_song['song_musician_fans']) == song.song_musician_fans.count()
