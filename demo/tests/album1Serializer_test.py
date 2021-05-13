from datetime import datetime

import factory
from django.test import TestCase
from django.urls import reverse
from rest_framework import serializers
from rest_framework.test import APIRequestFactory

from demo.serializers import Album1Serializer

from .factories import AlbumFactory


class Album1Serializer_Test(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.album = AlbumFactory.create()

    def test_that_a_album_is_correctly_serialized(self):
        album = self.album
        serializer = Album1Serializer
        serialized_album = serializer(album).data

        assert serialized_album['id'] == album.id
        assert serialized_album['name'] == album.name
