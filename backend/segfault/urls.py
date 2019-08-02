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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from .views import NaverLoginView, KakaoLoginView, GoogleLoginView

urlpatterns = [
    # admin
    path('admin/', admin.site.urls),
    # auth
    path(r'password-reset/confirm/<uidb64>/<token>/',
         TemplateView.as_view(template_name="password_reset_confirm.html"),
         name='password_reset_confirm'
         ),
    path('account/', include('allauth.urls')),
    path('rest-auth/', include('rest_auth.urls')),
    path('rest-auth/registration/', include('rest_auth.registration.urls')),
    path('rest-auth/naver/', NaverLoginView.as_view(), name='naver_login'),
    path('rest-auth/kakao/', KakaoLoginView.as_view(), name='kakao_login'),
    path('rest-auth/google/', GoogleLoginView.as_view(), name='google_login'),
    # apps
    path('api/', include('api.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
