from django.urls import path, include
from .views import NaverLoginView, KakaoLoginView, GoogleLoginView

app_name = 'auth'

urlpatterns = [
    path('', include('rest_auth.urls')),
    path('registration/', include('rest_auth.registration.urls')),
    path('o/naver/', NaverLoginView.as_view(), name='naver_login'),
    path('o/kakao/', KakaoLoginView.as_view(), name='kakao_login'),
    path('o/google/', GoogleLoginView.as_view(), name='google_login')
]
