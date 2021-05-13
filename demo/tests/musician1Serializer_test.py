from datetime import datetime

import factory
from django.test import TestCase
from django.urls import reverse
from rest_framework import serializers
from rest_framework.test import APIRequestFactory

from demo.serializers import Musician1Serializer

from .factories import MusicianFactory


class Musician1Serializer_Test(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.musician = MusicianFactory.create()

    def test_that_a_musician_is_correctly_serialized(self):
        musician = self.musician
        serializer = Musician1Serializer
        serialized_musician = serializer(musician).data

        assert serialized_musician['id'] == str(musician.id)
