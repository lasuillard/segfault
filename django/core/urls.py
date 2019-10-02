"""segfault URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import logging
import os
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

# media file services for dev-only
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
        logger.info('Create social application for service: {}'.format(sapp.provider))
except KeyError:
    # when secret.json is not available, add apps by environment variables.
    # naver.
    sapp = register_social_app(
        provider='naver',
        name='Naver',
        client_id=os.environ.get('NAVER_OAUTH2_CLIENT_ID'),
        secret=os.environ.get('NAVER_OAUTH2_CLIENT_SECRET')
    )
    logger.info('Create social application for service: {}'.format(sapp.provider))
    # kakao
    sapp = register_social_app(
        provider='kakao',
        name='Kakao',
        client_id=os.environ.get('KAKAO_OAUTH2_CLIENT_ID'),
        secret=os.environ.get('KAKAO_OAUTH2_CLIENT_SECRET')
    )
    logger.info('Create social application for service: {}'.format(sapp.provider))
    # google
    sapp = register_social_app(
        provider='google',
        name='Google',
        client_id=os.environ.get('GOOGLE_OAUTH2_CLIENT_ID'),
        secret=os.environ.get('GOOGLE_OAUTH2_CLIENT_SECRET')
    )
    logger.info('Create social application for service: {}'.format(sapp.provider))

except ProgrammingError:
    """
    When manage.py executed, i guess this root url also called(or imported).
    and it drives application into crash, so just simply pass it.
    """
    pass
