from django.views.generic import View
from django.shortcuts import HttpResponse
from allauth.socialaccount.providers.naver.views import NaverOAuth2Adapter
from allauth.socialaccount.providers.kakao.views import KakaoOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from rest_auth.registration.views import SocialLoginView, SocialConnectView


class NaverLoginView(SocialLoginView):
    adapter_class = NaverOAuth2Adapter
    callback_url = '/rest-auth/naver/'
    client_class = OAuth2Client


class KakaoLoginView(SocialLoginView):
    adapter_class = KakaoOAuth2Adapter
    callback_url = '/rest-auth/kakao/'
    client_class = OAuth2Client


class StatusView(View):
    def get(self, request):
        print(request.COOKIES)
        return HttpResponse(request.user.is_active)


class CloseView(View):
    def get(self, _):
        return HttpResponse('<script>window.close()</script>')

