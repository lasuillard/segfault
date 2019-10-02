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
from django.core.exceptions import ImproperlyConfigured
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
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
secret = settings.SECRETS
try:
    oauth = secret['OAUTH']
    for service in oauth:
        # get_or_create social application
        sapp, _ = SocialApp.objects.get_or_create(
            provider=service['PROVIDER'],
            name=service['NAME'],  # just an alias for it
            client_id=service['CLIENT_ID'],
            secret=service['CLIENT_SECRET']
        )
        # if current site is not registered, register it.
        if sapp.sites.filter(pk=settings.SITE_ID).count() == 0:
            sapp.sites.add(settings.SITE_ID)

        logger.info('Create social application for service: {}'.format(sapp.provider))
except KeyError:
    raise ImproperlyConfigured('secret.json has malformed oauth service definitions')
