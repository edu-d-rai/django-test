import json
from datetime import datetime

import factory
from django.core import management
from django.test import TestCase
from django.urls import reverse
from faker import Factory
from rest_framework import status
from rest_framework.test import APIClient

from ..models import Album
from .factories import AlbumFactory, MusicianFactory, SongFactory

faker = Factory.create()


class AlbumApi_Test(TestCase):
    def setUp(self):
        self.api_client = APIClient()
        AlbumFactory.create_batch(size=3)
        self.producer = MusicianFactory.create()

    def test_create_album(self):
        """
        Ensure we can create a new album object.
        """
        client = self.api_client
        album_count = Album.objects.count()
        album_dict = factory.build(dict, FACTORY_CLASS=AlbumFactory, producer=self.producer.id)
        response = client.post(reverse('album-api-list'), album_dict)
        created_album_pk = response.data['id']
        assert response.status_code == status.HTTP_201_CREATED
        assert Album.objects.count() == album_count + 1
        album = Album.objects.get(pk=created_album_pk)

        assert album_dict['name'] == album.name
        assert album_dict['genre'] == album.genre
        assert album_dict['num_stars'] == album.num_stars
        assert album_dict['ranking'] == album.ranking
        assert album_dict['upc'] == album.upc
        assert album_dict['release_date'] == str(album.release_date)

    def test_create_album_with_m2m_relations(self):
        client = self.api_client

        interpreters = MusicianFactory.create_batch(size=3)
        interpreters_pks = [musician.pk for musician in interpreters]

        collaborators = MusicianFactory.create_batch(size=3)
        collaborators_pks = [musician.pk for musician in collaborators]

        album_dict = factory.build(dict, FACTORY_CLASS=AlbumFactory, producer=self.producer.pk,
                                   interpreters=interpreters_pks, collaborators=collaborators_pks)

        response = client.post(reverse('album-api-list'), album_dict)
        created_album_pk = response.data['id']
        assert response.status_code == status.HTTP_201_CREATED

        album = Album.objects.get(pk=created_album_pk)
        assert interpreters[0].albums.first().pk == album.pk
        assert album.interpreters.count() == len(interpreters)
        assert collaborators[0].collab_albums.first().pk == album.pk
        assert album.collaborators.count() == len(collaborators)

    def test_get_one(self):
        client = self.api_client
        album_pk = Album.objects.first().pk
        album_detail_url = reverse('album-api-detail', kwargs={'pk': album_pk})
        response = client.get(album_detail_url)
        assert response.status_code == status.HTTP_200_OK

    def test_fetch_all(self):
        """
        Create 3 objects, do a fetch all call and check if you get back 3 objects
        """
        client = self.api_client
        response = client.get(reverse('album-api-list'))
        assert response.status_code == status.HTTP_200_OK
        assert Album.objects.count() == len(response.data)

    def test_delete(self):
        """
        Create 3 objects, do a fetch all call and check if you get back 3 objects.
        Then in a loop, delete one at a time and check that you get the correct number back on a fetch all.
        """
        client = self.api_client
        album_qs = Album.objects.all()
        album_count = Album.objects.count()

        for i, album in enumerate(album_qs, start=1):
            response = client.delete(reverse('album-api-detail', kwargs={'pk': album.pk}))
            assert response.status_code == status.HTTP_204_NO_CONTENT
            assert album_count - i == Album.objects.count()

    def test_update_correct(self):
        """
        Add an object. Call an update with 2 (or more) fields updated.
        Fetch the object back and confirm that the update was successful.
        """
        client = self.api_client
        album_pk = Album.objects.first().pk
        album_detail_url = reverse('album-api-detail', kwargs={'pk': album_pk})
        album_dict = factory.build(dict, FACTORY_CLASS=AlbumFactory, producer=self.producer.id)
        response = client.patch(album_detail_url, data=album_dict)
        assert response.status_code == status.HTTP_200_OK

        assert album_dict['name'] == response.data['name']
        assert album_dict['genre'] == response.data['genre']
        assert album_dict['release_date'] == response.data['release_date']
        assert album_dict['num_stars'] == response.data['num_stars']
        assert album_dict['ranking'] == response.data['ranking']
        assert album_dict['upc'] == response.data['upc']

    def test_update_release_date_with_incorrect_value_data_type(self):
        client = self.api_client
        album = Album.objects.first()
        album_detail_url = reverse('album-api-detail', kwargs={'pk': album.pk})
        album_release_date = album.release_date
        data = {
            'release_date': faker.pystr(),
        }
        response = client.patch(album_detail_url, data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert album_release_date == Album.objects.first().release_date

    def test_update_num_stars_with_incorrect_value_data_type(self):
        client = self.api_client
        album = Album.objects.first()
        album_detail_url = reverse('album-api-detail', kwargs={'pk': album.pk})
        album_num_stars = album.num_stars
        data = {
            'num_stars': faker.pystr(),
        }
        response = client.patch(album_detail_url, data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert album_num_stars == Album.objects.first().num_stars

    def test_update_ranking_with_incorrect_value_data_type(self):
        client = self.api_client
        album = Album.objects.first()
        album_detail_url = reverse('album-api-detail', kwargs={'pk': album.pk})
        album_ranking = album.ranking
        data = {
            'ranking': faker.pystr(),
        }
        response = client.patch(album_detail_url, data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert album_ranking == Album.objects.first().ranking

    def test_update_name_with_incorrect_value_outside_constraints(self):
        client = self.api_client
        album = Album.objects.first()
        album_detail_url = reverse('album-api-detail', kwargs={'pk': album.pk})
        album_name = album.name
        data = {
            'name': faker.pystr(min_chars=81, max_chars=81),
        }
        response = client.patch(album_detail_url, data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert album_name == Album.objects.first().name

    def test_update_num_stars_with_incorrect_value_outside_constraints(self):
        client = self.api_client
        album = Album.objects.first()
        album_detail_url = reverse('album-api-detail', kwargs={'pk': album.pk})
        album_num_stars = album.num_stars
        data = {
            'num_stars': faker.pyint(min_value=6),
        }
        response = client.patch(album_detail_url, data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert album_num_stars == Album.objects.first().num_stars

    def test_update_ranking_with_incorrect_value_outside_constraints(self):
        client = self.api_client
        album = Album.objects.first()
        album_detail_url = reverse('album-api-detail', kwargs={'pk': album.pk})
        album_ranking = album.ranking
        data = {
            'ranking': faker.pyint(min_value=12),
        }
        response = client.patch(album_detail_url, data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert album_ranking == Album.objects.first().ranking

    def test_update_upc_with_incorrect_value_outside_constraints(self):
        client = self.api_client
        album = Album.objects.first()
        album_detail_url = reverse('album-api-detail', kwargs={'pk': album.pk})
        album_upc = album.upc
        data = {
            'upc': faker.pystr(min_chars=13, max_chars=13),
        }
        response = client.patch(album_detail_url, data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert album_upc == Album.objects.first().upc
