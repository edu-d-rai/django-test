import uuid
from django.db import models

class Song(models.Model) :

    album = models.ForeignKey('Album', to_field='name', on_delete=models.CASCADE, related_name='songs')
    composer = models.ForeignKey('Musician', on_delete=models.CASCADE, related_name='composed_songs')
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    lyrics = models.CharField(max_length=1000, null=True, blank=True)
    code = models.UUIDField(null=True, blank=True, default=uuid.uuid4, editable=False)

