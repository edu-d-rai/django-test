from datetime import datetime

import factory
from django.test import TestCase
from django.urls import reverse
from rest_framework import serializers
from rest_framework.test import APIRequestFactory

from demo.serializers import AlbumSerializer

from .factories import (
    AlbumFactory,
    AlbumWithForeignFactory,
    MusicianFactory,
    SongFactory,
)


class AlbumSerializer_Test(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.album = AlbumWithForeignFactory.create()

    def test_that_a_album_is_correctly_serialized(self):
        album = self.album
        serializer = AlbumSerializer
        serialized_album = serializer(album).data

        assert serialized_album['id'] == album.id
        assert serialized_album['name'] == album.name
        assert serialized_album['genre'] == album.genre
        assert serialized_album['release_date'] == album.release_date
        assert serialized_album['num_stars'] == album.num_stars
        assert serialized_album['ranking'] == album.ranking
        assert serialized_album['upc'] == album.upc
        assert serialized_album['release_date'] == str(album.release_date)

        assert len(serialized_album['songs']) == album.songs.count()
