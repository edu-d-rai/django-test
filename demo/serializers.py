from rest_framework import serializers
from .models import Musician, Album, Concert, Song

class MusicianSerializer(serializers.ModelSerializer) :

    prod_records = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Album.objects.all(),
        required=False
    )

    main_concerts = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Concert.objects.all(),
        required=False
    )

    secondary_concerts = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Concert.objects.all(),
        required=False
    )

    influenced_musicians = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Musician.objects.all(),
        required=False
    )

    composed_songs = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Song.objects.all(),
        required=False
    )

    influencer = serializers.PrimaryKeyRelatedField(
        queryset=Musician.objects.all(),
        required=False
    )

    preferred_song = serializers.PrimaryKeyRelatedField(
        queryset=Song.objects.all(),
        required=False
    )
    albums = serializers.PrimaryKeyRelatedField(
        queryset=Album.objects.all(),
        many=True,
        required=False
    )
    collab_albums = serializers.PrimaryKeyRelatedField(
        queryset=Album.objects.all(),
        many=True,
        required=False
    )

    class Meta :
        model = Musician
        fields = ['id', 'first_name', 'last_name', 'instrument', 'age', 'fans', 'inspired_at', 'prod_records', 'main_concerts', 'secondary_concerts', 'influenced_musicians', 'composed_songs', 'influencer', 'preferred_song', 'albums', 'collab_albums']

class AlbumSerializer(serializers.ModelSerializer) :

    songs = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Song.objects.all(),
        required=False
    )

    producer = serializers.PrimaryKeyRelatedField(
        queryset=Musician.objects.all(),
        required=False
    )
    interpreters = serializers.PrimaryKeyRelatedField(
        queryset=Musician.objects.all(),
        many=True,
        required=False
    )
    collaborators = serializers.PrimaryKeyRelatedField(
        queryset=Musician.objects.all(),
        many=True,
        required=False
    )

    class Meta :
        model = Album
        fields = ['id', 'name', 'genre', 'release_date', 'num_stars', 'ranking', 'upc', 'songs', 'producer', 'interpreters', 'collaborators']

class SongSerializer(serializers.ModelSerializer) :

    song_musician_fans = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Musician.objects.all(),
        required=False
    )

    album = serializers.PrimaryKeyRelatedField(
        queryset=Album.objects.all(),
    )

    composer = serializers.PrimaryKeyRelatedField(
        queryset=Musician.objects.all(),
    )

    class Meta :
        model = Song
        fields = ['id', 'name', 'lyrics', 'code', 'song_musician_fans', 'album', 'composer']

class ConcertSerializer(serializers.ModelSerializer) :

    main_artist = serializers.PrimaryKeyRelatedField(
        queryset=Musician.objects.all(),
    )

    secondary_artist = serializers.PrimaryKeyRelatedField(
        queryset=Musician.objects.all(),
        required=False
    )

    class Meta :
        model = Concert
        fields = ['name', 'place', 'date', 'is_free', 'main_artist', 'secondary_artist']

class Musician1Serializer(serializers.ModelSerializer) :

    influencer = serializers.PrimaryKeyRelatedField(
        queryset=Musician.objects.all(),
        required=False
    )

    class Meta :
        model = Musician
        fields = ['id', 'influencer']

class Musician2Serializer(serializers.ModelSerializer) :

    prod_records = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Album.objects.all(),
        required=False
    )

    class Meta :
        model = Musician
        fields = ['id', 'first_name', 'last_name', 'prod_records']

class Album1Serializer(serializers.ModelSerializer) :

    class Meta :
        model = Album
        fields = ['id', 'name']

