# Generated by Django 3.2.1 on 2021-05-04 18:54

import datetime
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Album',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=80, unique=True)),
                ('genre', models.IntegerField(blank=True, choices=[(1, 'ROCK'), (2, 'POP'), (3, 'FOLK')], null=True)),
                ('release_date', models.DateField(blank=True, default=datetime.date.today, null=True)),
                ('num_stars', models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)])),
                ('ranking', models.FloatField(blank=True, default=3.0, null=True, validators=[django.core.validators.MinValueValidator(2.0), django.core.validators.MaxValueValidator(10.2)])),
                ('upc', models.CharField(blank=True, max_length=12, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Musician',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('first_name', models.CharField(blank=True, max_length=70, null=True)),
                ('last_name', models.CharField(blank=True, max_length=40, null=True)),
                ('instrument', models.IntegerField(blank=True, choices=[(1, 'GUITAR'), (2, 'PIANO'), (3, 'DRUMS'), (4, 'BASS'), (5, 'VOICE')], null=True)),
                ('age', models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0)])),
                ('fans', models.BigIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0)])),
                ('inspired_at', models.TimeField(blank=True, null=True)),
                ('influencer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='influenced_musicians', to='demo.musician')),
            ],
        ),
        migrations.CreateModel(
            name='Song',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('lyrics', models.CharField(blank=True, max_length=1000, null=True)),
                ('code', models.UUIDField(blank=True, default=uuid.uuid4, editable=False, null=True)),
                ('album', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='songs', to='demo.album', to_field='name')),
                ('composer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='composed_songs', to='demo.musician')),
            ],
        ),
        migrations.AddField(
            model_name='musician',
            name='preferred_song',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='song_musician_fans', to='demo.song'),
        ),
        migrations.CreateModel(
            name='Concert',
            fields=[
                ('name', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('place', models.CharField(max_length=200)),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_free', models.BooleanField(blank=True, null=True)),
                ('main_artist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='main_concerts', to='demo.musician')),
                ('secondary_artist', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='secondary_concerts', to='demo.musician')),
            ],
        ),
        migrations.AddField(
            model_name='album',
            name='collaborators',
            field=models.ManyToManyField(blank=True, db_table='records_collaborators', related_name='collab_albums', to='demo.Musician'),
        ),
        migrations.AddField(
            model_name='album',
            name='interpreters',
            field=models.ManyToManyField(blank=True, db_table='records_interpreters', related_name='albums', to='demo.Musician'),
        ),
        migrations.AddField(
            model_name='album',
            name='producer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='prod_records', to='demo.musician'),
        ),
    ]