import factory
import json
from datetime import datetime
from django.core import management
from django.test import TestCase
from django.urls import reverse
from faker import Factory
from rest_framework import status
from rest_framework.test import APIClient

from ..models import Musician
from .factories import MusicianFactory, SongFactory, AlbumFactory, ConcertFactory

faker = Factory.create()

class MusicianFetchInfluencer_Test(TestCase):
    def setUp(self):
        self.api_client = APIClient()
        MusicianFactory.create_batch(size=3)
        self.influencer = MusicianFactory.create()


    def test_get_one(self):
        client = self.api_client
        musician_pk = Musician.objects.first().pk
        musician_detail_url = reverse('musician-fetch-influencer-detail', kwargs={'pk': musician_pk})
        response = client.get(musician_detail_url)
        assert response.status_code == status.HTTP_200_OK
    



