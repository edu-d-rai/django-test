from rest_framework import viewsets
from .models import Musician, Album, Song, Concert
from .serializers import MusicianSerializer, AlbumSerializer, SongSerializer, ConcertSerializer

class MusicianApiViewSet(viewsets.ModelViewSet) :
    queryset = Musician.objects.all()
    serializer_class = MusicianSerializer
    permission_classes = []
    filterset_fields = ['id', 'first_name', 'last_name', 'instrument', 'age', 'fans', 'inspired_at', 'prod_records', 'main_concerts', 'secondary_concerts', 'influenced_musicians', 'composed_songs', 'influencer', 'preferred_song']

class AlbumApiViewSet(viewsets.ModelViewSet) :
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer
    permission_classes = []
    filterset_fields = ['id', 'name', 'genre', 'release_date', 'num_stars', 'ranking', 'upc', 'songs', 'producer']

class SongApiViewSet(viewsets.ModelViewSet) :
    queryset = Song.objects.all()
    serializer_class = SongSerializer
    permission_classes = []
    filterset_fields = ['id', 'name', 'lyrics', 'code', 'song_musician_fans', 'album', 'composer']

class ConcertApiViewSet(viewsets.ModelViewSet) :
    queryset = Concert.objects.all()
    serializer_class = ConcertSerializer
    permission_classes = []
    filterset_fields = ['name', 'place', 'date', 'is_free', 'main_artist', 'secondary_artist']

