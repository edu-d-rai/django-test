from django.conf.urls import include, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.routers import DefaultRouter

from .views import (
    AlbumApiViewSet,
    ConcertApiViewSet,
    GetAlbumsByStarsViewSet,
    GetAlbumSongsViewSet,
    MusicianApiViewSet,
    MusicianFetchAllViewSet,
    MusicianFetchInfluencerViewSet,
    MusicianOnlyFetchApiViewSet,
    MusicianUpdateInfluencerViewSet,
    SongApiViewSet,
)

router = DefaultRouter()

router.register(r'musician-api', MusicianApiViewSet, 'musician-api')
router.register(r'album-api', AlbumApiViewSet, 'album-api')
router.register(r'song-api', SongApiViewSet, 'song-api')
router.register(r'concert-api', ConcertApiViewSet, 'concert-api')
router.register(r'musician-fetch-influencer', MusicianFetchInfluencerViewSet, 'musician-fetch-influencer')
router.register(r'musician-update-influencer', MusicianUpdateInfluencerViewSet, 'musician-update-influencer')
router.register(r'musician-fetch-all', MusicianFetchAllViewSet, 'musician-fetch-all')
router.register(r'musician-only-fetch-api', MusicianOnlyFetchApiViewSet, 'musician-only-fetch-api')
router.register(r'get-albums-by-stars', GetAlbumsByStarsViewSet, 'get-albums-by-stars')
router.register(r'get-album-songs', GetAlbumSongsViewSet, 'get-album-songs')

schema_view = get_schema_view(
    openapi.Info(
        title="demo",
        default_version='v1',
        description="API description",
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    re_path('^', include(router.urls)),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
