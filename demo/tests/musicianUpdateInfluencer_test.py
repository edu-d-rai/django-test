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

class MusicianUpdateInfluencer_Test(TestCase):
    def setUp(self):
        self.api_client = APIClient()
        MusicianFactory.create_batch(size=3)
        self.influencer = MusicianFactory.create()


    


    def test_update_correct(self):
        """
        Add an object. Call an update with 2 (or more) fields updated.
        Fetch the object back and confirm that the update was successful.
        """
        client = self.api_client
        musician_pk = Musician.objects.first().pk
        musician_detail_url = reverse('musician-update-influencer-detail', kwargs={'pk': musician_pk})
        musician_dict = factory.build(dict, FACTORY_CLASS=MusicianFactory, influencer=self.influencer.id)
        response = client.patch(musician_detail_url, data=musician_dict)
        assert response.status_code == status.HTTP_200_OK

    

