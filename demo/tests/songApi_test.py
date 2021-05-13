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


class SongApi_Test(TestCase):
    def setUp(self):
        self.api_client = APIClient()
        SongFactory.create_batch(size=3)
        self.album = AlbumFactory.create()
        self.composer = MusicianFactory.create()

    def test_create_song(self):
        """
        Ensure we can create a new song object.
        """
        client = self.api_client
        song_count = Song.objects.count()
        song_dict = factory.build(dict, FACTORY_CLASS=SongFactory, album=self.album.id, composer=self.composer.id)
        response = client.post(reverse('song-api-list'), song_dict)
        created_song_pk = response.data['id']
        assert response.status_code == status.HTTP_201_CREATED
        assert Song.objects.count() == song_count + 1
        song = Song.objects.get(pk=created_song_pk)

        assert song_dict['id'] == song.id
        assert song_dict['name'] == song.name
        assert song_dict['lyrics'] == song.lyrics

    def test_get_one(self):
        client = self.api_client
        song_pk = Song.objects.first().pk
        song_detail_url = reverse('song-api-detail', kwargs={'pk': song_pk})
        response = client.get(song_detail_url)
        assert response.status_code == status.HTTP_200_OK

    def test_fetch_all(self):
        """
        Create 3 objects, do a fetch all call and check if you get back 3 objects
        """
        client = self.api_client
        response = client.get(reverse('song-api-list'))
        assert response.status_code == status.HTTP_200_OK
        assert Song.objects.count() == len(response.data)

    def test_delete(self):
        """
        Create 3 objects, do a fetch all call and check if you get back 3 objects.
        Then in a loop, delete one at a time and check that you get the correct number back on a fetch all.
        """
        client = self.api_client
        song_qs = Song.objects.all()
        song_count = Song.objects.count()

        for i, song in enumerate(song_qs, start=1):
            response = client.delete(reverse('song-api-detail', kwargs={'pk': song.pk}))
            assert response.status_code == status.HTTP_204_NO_CONTENT
            assert song_count - i == Song.objects.count()

    def test_update_correct(self):
        """
        Add an object. Call an update with 2 (or more) fields updated.
        Fetch the object back and confirm that the update was successful.
        """
        client = self.api_client
        song_pk = Song.objects.first().pk
        song_detail_url = reverse('song-api-detail', kwargs={'pk': song_pk})
        song_dict = factory.build(dict, FACTORY_CLASS=SongFactory, album=self.album.id, composer=self.composer.id)
        song_dict.pop('id')
        response = client.patch(song_detail_url, data=song_dict)
        assert response.status_code == status.HTTP_200_OK

        assert song_pk == response.data['id']
        assert song_dict['name'] == response.data['name']
        assert song_dict['lyrics'] == response.data['lyrics']

    def test_update_id_with_incorrect_value_data_type(self):
        client = self.api_client
        song = Song.objects.first()
        song_detail_url = reverse('song-api-detail', kwargs={'pk': song.pk})
        song_id = song.id
        data = {
            'id': faker.pystr(),
        }
        response = client.patch(song_detail_url, data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert song_id == Song.objects.first().id

    def test_update_name_with_incorrect_value_outside_constraints(self):
        client = self.api_client
        song = Song.objects.first()
        song_detail_url = reverse('song-api-detail', kwargs={'pk': song.pk})
        song_name = song.name
        data = {
            'name': faker.pystr(min_chars=101, max_chars=101),
        }
        response = client.patch(song_detail_url, data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert song_name == Song.objects.first().name

    def test_update_lyrics_with_incorrect_value_outside_constraints(self):
        client = self.api_client
        song = Song.objects.first()
        song_detail_url = reverse('song-api-detail', kwargs={'pk': song.pk})
        song_lyrics = song.lyrics
        data = {
            'lyrics': faker.pystr(min_chars=1001, max_chars=1001),
        }
        response = client.patch(song_detail_url, data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert song_lyrics == Song.objects.first().lyrics
