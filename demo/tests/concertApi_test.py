import factory
import json
from datetime import datetime
from django.core import management
from django.test import TestCase
from django.urls import reverse
from faker import Factory
from rest_framework import status
from rest_framework.test import APIClient

from ..models import Concert
from .factories import ConcertFactory, MusicianFactory

faker = Factory.create()

class ConcertApi_Test(TestCase):
    def setUp(self):
        self.api_client = APIClient()
        ConcertFactory.create_batch(size=3)
        self.main_artist = MusicianFactory.create()
        self.secondary_artist = MusicianFactory.create()

    def test_create_concert(self):
        """
        Ensure we can create a new concert object.
        """
        client = self.api_client
        concert_count = Concert.objects.count()
        concert_dict = factory.build(dict, FACTORY_CLASS=ConcertFactory, main_artist=self.main_artist.id, secondary_artist=self.secondary_artist.id)
        response = client.post(reverse('concert-api-list'), concert_dict)
        created_concert_pk = response.data['name']
        assert response.status_code == status.HTTP_201_CREATED
        assert Concert.objects.count() == concert_count + 1
        concert = Concert.objects.get(pk=created_concert_pk)

        assert concert_dict['name'] == concert.name
        assert concert_dict['place'] == concert.place
        assert concert_dict['is_free'] == concert.is_free
        assert concert_dict['date'] == concert.date.isoformat()

    def test_get_one(self):
        client = self.api_client
        concert_pk = Concert.objects.first().pk
        concert_detail_url = reverse('concert-api-detail', kwargs={'pk': concert_pk})
        response = client.get(concert_detail_url)
        assert response.status_code == status.HTTP_200_OK
    
    def test_fetch_all(self):
        """
        Create 3 objects, do a fetch all call and check if you get back 3 objects
        """
        client = self.api_client
        response = client.get(reverse('concert-api-list'))
        assert response.status_code == status.HTTP_200_OK
        assert Concert.objects.count() == len(response.data)

    def test_delete(self):
        """
        Create 3 objects, do a fetch all call and check if you get back 3 objects.
        Then in a loop, delete one at a time and check that you get the correct number back on a fetch all.
        """
        client = self.api_client
        concert_qs = Concert.objects.all()
        concert_count = Concert.objects.count()

        for i, concert in enumerate(concert_qs, start=1):
            response = client.delete(reverse('concert-api-detail', kwargs={'pk': concert.pk}))
            assert response.status_code == status.HTTP_204_NO_CONTENT
            assert concert_count - i == Concert.objects.count()

    def test_update_correct(self):
        """
        Add an object. Call an update with 2 (or more) fields updated.
        Fetch the object back and confirm that the update was successful.
        """
        client = self.api_client
        concert_pk = Concert.objects.first().pk
        concert_detail_url = reverse('concert-api-detail', kwargs={'pk': concert_pk})
        concert_dict = factory.build(dict, FACTORY_CLASS=ConcertFactory, main_artist=self.main_artist.id, secondary_artist=self.secondary_artist.id)
        concert_dict.pop('name')
        response = client.patch(concert_detail_url, data=concert_dict)
        assert response.status_code == status.HTTP_200_OK

        assert concert_pk == response.data['name']
        assert concert_dict['place'] == response.data['place']
        assert concert_dict['date'] == response.data['date'].replace('Z', '+00:00')
        assert concert_dict['is_free'] == response.data['is_free']
    
    def test_update_date_with_incorrect_value_data_type(self):
        client = self.api_client
        concert = Concert.objects.first()
        concert_detail_url = reverse('concert-api-detail', kwargs={'pk': concert.pk})
        concert_date = concert.date
        data = {
            'date': faker.pystr(),
        }
        response = client.patch(concert_detail_url, data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert concert_date == Concert.objects.first().date

    def test_update_is_free_with_incorrect_value_data_type(self):
        client = self.api_client
        concert = Concert.objects.first()
        concert_detail_url = reverse('concert-api-detail', kwargs={'pk': concert.pk})
        concert_is_free = concert.is_free
        data = {
            'is_free': faker.pystr(),
        }
        response = client.patch(concert_detail_url, data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert concert_is_free == Concert.objects.first().is_free

    def test_update_name_with_incorrect_value_outside_constraints(self):
        client = self.api_client
        concert = Concert.objects.first()
        concert_detail_url = reverse('concert-api-detail', kwargs={'pk': concert.pk})
        concert_name = concert.name
        data = {
            'name': faker.pystr(min_chars=51, max_chars=51),
        }
        response = client.patch(concert_detail_url, data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert concert_name == Concert.objects.first().name

    def test_update_place_with_incorrect_value_outside_constraints(self):
        client = self.api_client
        concert = Concert.objects.first()
        concert_detail_url = reverse('concert-api-detail', kwargs={'pk': concert.pk})
        concert_place = concert.place
        data = {
            'place': faker.pystr(min_chars=201, max_chars=201),
        }
        response = client.patch(concert_detail_url, data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert concert_place == Concert.objects.first().place


