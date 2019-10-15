import logging
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.db.utils import ProgrammingError
from django.urls import path, include
from allauth.socialaccount.models import SocialApp

logger = logging.getLogger(__name__)

urlpatterns = [
    path('accounts/', include('allauth.urls')),
    # admin urls
    path('admin/', admin.site.urls),
    path('admin/doc/', include('django.contrib.admindocs.urls')),
    # auth urls
    path('auth/', include('auth.urls')),
    # apps urls
    path('api/', include('api.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# create social apps for oauth support, with 'secret.json' file.
def register_social_app(provider, name, client_id, secret):
    # get_or_create social application
    sapp, _ = SocialApp.objects.get_or_create(
        provider=provider,
        name=name,
        client_id=client_id,
        secret=secret
    )
    # if current site is not registered, register it.
    if sapp.sites.filter(pk=settings.SITE_ID).count() == 0:
        sapp.sites.add(settings.SITE_ID)
    logger.info('Created social application for service: {}'.format(sapp.provider))
    return sapp


secret_json = settings.SECRETS
try:
    oauth = secret_json['OAUTH']
    for service in oauth:
        sapp = register_social_app(
            provider=service['PROVIDER'],
            name=service['NAME'],
            client_id=service['CLIENT_ID'],
            secret=service['CLIENT_SECRET']
        )
except KeyError as e:
    logger.critical('Erroneous configuration file or env: {}'.format(e))
except ProgrammingError as e:
    """
    When manage.py executed, i guess this root url also called(or imported).
    and it drives application into crash, so just simply pass it.
    """
    logger.warning('Skipping error handling in initializing configuration: {}'.format(e))
