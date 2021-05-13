import factory
from datetime import datetime
from django.test import TestCase
from django.urls import reverse
from rest_framework import serializers
from rest_framework.test import APIRequestFactory
from .factories import ConcertFactory
from demo.serializers import ConcertSerializer

class ConcertSerializer_Test(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.concert = ConcertFactory.create()

    def test_that_a_concert_is_correctly_serialized(self):
        concert = self.concert
        serializer = ConcertSerializer
        serialized_concert = serializer(concert).data

        assert serialized_concert['name'] == concert.name
        assert serialized_concert['place'] == concert.place
        assert serialized_concert['date'] == concert.date
        assert serialized_concert['is_free'] == concert.is_free

