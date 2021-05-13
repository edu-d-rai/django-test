from rest_framework import mixins, viewsets

from .models import Album, Concert, Musician, Song
from .serializers import (
    Album1Serializer,
    AlbumSerializer,
    ConcertSerializer,
    Musician1Serializer,
    Musician2Serializer,
    MusicianSerializer,
    SongSerializer,
)


class MusicianApiViewSet(viewsets.ModelViewSet):
    queryset = Musician.objects.all()
    serializer_class = MusicianSerializer
    permission_classes = []
    filterset_fields = ['id', 'first_name', 'last_name', 'instrument', 'age', 'fans', 'inspired_at', 'prod_records',
                        'main_concerts', 'secondary_concerts', 'influenced_musicians', 'composed_songs', 'influencer', 'preferred_song']


class AlbumApiViewSet(viewsets.ModelViewSet):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer
    permission_classes = []
    filterset_fields = ['id', 'name', 'genre', 'release_date', 'num_stars', 'ranking', 'upc', 'songs', 'producer']


class SongApiViewSet(viewsets.ModelViewSet):
    queryset = Song.objects.all()
    serializer_class = SongSerializer
    permission_classes = []
    filterset_fields = ['id', 'name', 'lyrics', 'code', 'song_musician_fans', 'album', 'composer']


class ConcertApiViewSet(viewsets.ModelViewSet):
    queryset = Concert.objects.all()
    serializer_class = ConcertSerializer
    permission_classes = []
    filterset_fields = ['name', 'place', 'date', 'is_free', 'main_artist', 'secondary_artist']


class MusicianFetchInfluencerViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin):
    queryset = Musician.objects.all()
    serializer_class = Musician1Serializer
    permission_classes = []


class MusicianUpdateInfluencerViewSet(viewsets.GenericViewSet, mixins.UpdateModelMixin):
    queryset = Musician.objects.all()
    serializer_class = Musician1Serializer
    permission_classes = []


class MusicianFetchAllViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    queryset = Musician.objects.all()
    serializer_class = MusicianSerializer
    permission_classes = []
    filterset_fields = ['id', 'first_name', 'last_name']


class MusicianOnlyFetchApiViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin, mixins.ListModelMixin):
    queryset = Musician.objects.all()
    serializer_class = Musician2Serializer
    permission_classes = []
    filterset_fields = ['id', 'first_name', 'last_name', 'instrument', 'age', 'fans', 'inspired_at', 'prod_records',
                        'main_concerts', 'secondary_concerts', 'influenced_musicians', 'composed_songs', 'influencer', 'preferred_song']


class GetAlbumsByStarsViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = Album.objects.all()
    serializer_class = Album1Serializer
    permission_classes = []
    filterset_fields = ['num_stars']


class GetAlbumSongsViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = Song.objects.all()
    serializer_class = SongSerializer
    permission_classes = []
    filterset_fields = ['album']
