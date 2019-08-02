from django.views.generic import View
from django.shortcuts import HttpResponse
from allauth.socialaccount.providers.naver.views import NaverOAuth2Adapter
from allauth.socialaccount.providers.kakao.views import KakaoOAuth2Adapter
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from rest_auth.registration.views import SocialLoginView, SocialConnectView

CALLBACK_URL = 'http://localhost:3000/auth/o/'


class NaverLoginView(SocialLoginView):
    client_class = OAuth2Client
    adapter_class = NaverOAuth2Adapter
    callback_url = CALLBACK_URL


class KakaoLoginView(SocialLoginView):
    client_class = OAuth2Client
    adapter_class = KakaoOAuth2Adapter
    callback_url = CALLBACK_URL


class GoogleLoginView(SocialLoginView):
    client_class = OAuth2Client
    adapter_class = GoogleOAuth2Adapter
    callback_url = CALLBACK_URL
