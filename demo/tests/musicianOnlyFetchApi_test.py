import json
from datetime import datetime

import factory
from django.core import management
from django.test import TestCase
from django.urls import reverse
from faker import Factory
from rest_framework import status
from rest_framework.test import APIClient

from ..models import Musician
from .factories import (
    AlbumFactory,
    ConcertFactory,
    MusicianFactory,
    SongFactory,
)

faker = Factory.create()


class MusicianOnlyFetchApi_Test(TestCase):
    def setUp(self):
        self.api_client = APIClient()
        MusicianFactory.create_batch(size=3)

    def test_get_one(self):
        client = self.api_client
        musician_pk = Musician.objects.first().pk
        musician_detail_url = reverse('musician-only-fetch-api-detail', kwargs={'pk': musician_pk})
        response = client.get(musician_detail_url)
        assert response.status_code == status.HTTP_200_OK

    def test_fetch_all(self):
        """
        Create 3 objects, do a fetch all call and check if you get back 3 objects
        """
        client = self.api_client
        response = client.get(reverse('musician-only-fetch-api-list'))
        assert response.status_code == status.HTTP_200_OK
        assert Musician.objects.count() == len(response.data)
