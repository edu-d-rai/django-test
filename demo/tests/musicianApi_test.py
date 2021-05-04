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

class MusicianApi_Test(TestCase):
    def setUp(self):
        self.api_client = APIClient()
        MusicianFactory.create_batch(size=3)
        self.influencer = MusicianFactory.create()
        self.preferred_song = SongFactory.create()

    def test_create_musician(self):
        """
        Ensure we can create a new musician object.
        """
        client = self.api_client
        musician_count = Musician.objects.count()
        musician_dict = factory.build(dict, FACTORY_CLASS=MusicianFactory, influencer=self.influencer.id, preferred_song=self.preferred_song.id)
        response = client.post(reverse('musician-api-list'), musician_dict)
        created_musician_pk = response.data['id']
        assert response.status_code == status.HTTP_201_CREATED
        assert Musician.objects.count() == musician_count + 1
        musician = Musician.objects.get(pk=created_musician_pk)

        assert musician_dict['first_name'] == musician.first_name
        assert musician_dict['last_name'] == musician.last_name
        assert musician_dict['instrument'] == musician.instrument
        assert musician_dict['age'] == musician.age
        assert musician_dict['fans'] == musician.fans
        assert musician_dict['inspired_at'] == str(musician.inspired_at)
    
    def test_create_musician_with_m2m_relations(self):
        client = self.api_client
        
        albums = AlbumFactory.create_batch(size=3)
        albums_pks = [album.pk for album in albums]
        
        collab_albums = AlbumFactory.create_batch(size=3)
        collab_albums_pks = [album.pk for album in collab_albums]

        musician_dict = factory.build(dict, FACTORY_CLASS=MusicianFactory, influencer=self.influencer.pk, preferred_song=self.preferred_song.pk, albums=albums_pks, collab_albums=collab_albums_pks)
        
        response = client.post(reverse('musician-api-list'), musician_dict)
        created_musician_pk = response.data['id']
        assert response.status_code == status.HTTP_201_CREATED
        
        musician = Musician.objects.get(pk=created_musician_pk)
        assert albums[0].interpreters.first().pk == musician.pk
        assert musician.albums.count() == len(albums)
        assert collab_albums[0].collaborators.first().pk == musician.pk
        assert musician.collab_albums.count() == len(collab_albums)

    def test_get_one(self):
        client = self.api_client
        musician_pk = Musician.objects.first().pk
        musician_detail_url = reverse('musician-api-detail', kwargs={'pk': musician_pk})
        response = client.get(musician_detail_url)
        assert response.status_code == status.HTTP_200_OK
    
    def test_fetch_all(self):
        """
        Create 3 objects, do a fetch all call and check if you get back 3 objects
        """
        client = self.api_client
        response = client.get(reverse('musician-api-list'))
        assert response.status_code == status.HTTP_200_OK
        assert Musician.objects.count() == len(response.data)

    def test_delete(self):
        """
        Create 3 objects, do a fetch all call and check if you get back 3 objects.
        Then in a loop, delete one at a time and check that you get the correct number back on a fetch all.
        """
        client = self.api_client
        musician_qs = Musician.objects.all()
        musician_count = Musician.objects.count()

        for i, musician in enumerate(musician_qs, start=1):
            response = client.delete(reverse('musician-api-detail', kwargs={'pk': musician.pk}))
            assert response.status_code == status.HTTP_204_NO_CONTENT
            assert musician_count - i == Musician.objects.count()

    def test_update_correct(self):
        """
        Add an object. Call an update with 2 (or more) fields updated.
        Fetch the object back and confirm that the update was successful.
        """
        client = self.api_client
        musician_pk = Musician.objects.first().pk
        musician_detail_url = reverse('musician-api-detail', kwargs={'pk': musician_pk})
        musician_dict = factory.build(dict, FACTORY_CLASS=MusicianFactory, influencer=self.influencer.id, preferred_song=self.preferred_song.id)
        response = client.patch(musician_detail_url, data=musician_dict)
        assert response.status_code == status.HTTP_200_OK

        assert musician_dict['first_name'] == response.data['first_name']
        assert musician_dict['last_name'] == response.data['last_name']
        assert musician_dict['instrument'] == response.data['instrument']
        assert musician_dict['age'] == response.data['age']
        assert musician_dict['fans'] == response.data['fans']
        assert musician_dict['inspired_at'] == response.data['inspired_at']
    
    def test_update_age_with_incorrect_value_data_type(self):
        client = self.api_client
        musician = Musician.objects.first()
        musician_detail_url = reverse('musician-api-detail', kwargs={'pk': musician.pk})
        musician_age = musician.age
        data = {
            'age': faker.pystr(),
        }
        response = client.patch(musician_detail_url, data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert musician_age == Musician.objects.first().age

    def test_update_fans_with_incorrect_value_data_type(self):
        client = self.api_client
        musician = Musician.objects.first()
        musician_detail_url = reverse('musician-api-detail', kwargs={'pk': musician.pk})
        musician_fans = musician.fans
        data = {
            'fans': faker.pystr(),
        }
        response = client.patch(musician_detail_url, data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert musician_fans == Musician.objects.first().fans

    def test_update_inspired_at_with_incorrect_value_data_type(self):
        client = self.api_client
        musician = Musician.objects.first()
        musician_detail_url = reverse('musician-api-detail', kwargs={'pk': musician.pk})
        musician_inspired_at = musician.inspired_at
        data = {
            'inspired_at': faker.pystr(),
        }
        response = client.patch(musician_detail_url, data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert musician_inspired_at == Musician.objects.first().inspired_at

    def test_update_first_name_with_incorrect_value_outside_constraints(self):
        client = self.api_client
        musician = Musician.objects.first()
        musician_detail_url = reverse('musician-api-detail', kwargs={'pk': musician.pk})
        musician_first_name = musician.first_name
        data = {
            'first_name': faker.pystr(min_chars=71, max_chars=71),
        }
        response = client.patch(musician_detail_url, data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert musician_first_name == Musician.objects.first().first_name

    def test_update_last_name_with_incorrect_value_outside_constraints(self):
        client = self.api_client
        musician = Musician.objects.first()
        musician_detail_url = reverse('musician-api-detail', kwargs={'pk': musician.pk})
        musician_last_name = musician.last_name
        data = {
            'last_name': faker.pystr(min_chars=41, max_chars=41),
        }
        response = client.patch(musician_detail_url, data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert musician_last_name == Musician.objects.first().last_name


