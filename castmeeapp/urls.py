from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('artist_registration/', ArtistCreateAPIView.as_view(), name='artist_registration'),
    path('producer_registration/', ProducerCreateAPIView.as_view(), name='producer_registration'),
    path('login_artist/', ArtistLoginAPIView.as_view(), name='producer_registration'),
    path('login_producer/', ProducerLogin.as_view(), name='producer_registration'),
    path('dropdowns/', MasterDropdowns.as_view(), name='MasterDropdowns'),
    path('update_artist/', ArtistExtendedUpdateAPIView.as_view(), name='ArtistExtendedUpdateAPIView'),
    path('get_artist_user/', ArtistExtendedUpdateAPIView.as_view(), name='ArtistExtendedUpdateAPIView'),
    path('update_producer/', ProducerExtendedAPIView.as_view(), name='ProducerExtendedAPIView'),
    path('get_producer_user/', ProducerExtendedAPIView.as_view(), name='ProducerExtendedAPIView'),
    path('get_artists/', FilterApi.as_view(), name='FilterApi'),
    path('filter_artists/', FilterApi.as_view(), name='filter artists'),
]