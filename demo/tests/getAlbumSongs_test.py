import json
from datetime import datetime

import factory
from django.core import management
from django.test import TestCase
from django.urls import reverse
from faker import Factory
from rest_framework import status
from rest_framework.test import APIClient

from ..models import Song
from .factories import AlbumFactory, MusicianFactory, SongFactory

faker = Factory.create()


class GetAlbumSongs_Test(TestCase):
    def setUp(self):
        self.api_client = APIClient()
        SongFactory.create_batch(size=3)
        self.album = AlbumFactory.create()
        self.composer = MusicianFactory.create()

    def test_fetch_all(self):
        """
        Create 3 objects, do a fetch all call and check if you get back 3 objects
        """
        client = self.api_client
        response = client.get(reverse('get-album-songs-list'))
        assert response.status_code == status.HTTP_200_OK
        assert Song.objects.count() == len(response.data)
