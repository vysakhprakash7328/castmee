from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('artist_registration/', ArtistCreateAPIView.as_view(), name='artist_registration'),
    path('producer_registration/', ProducerCreateAPIView.as_view(), name='producer_registration'),
    path('login/', Login.as_view(), name='producer_registration'),
    path('dropdowns/', MasterDropdowns.as_view(), name='MasterDropdowns'),
    path('update_artist/', ArtistExtendedUpdateAPIView.as_view(), name='ArtistExtendedUpdateAPIView'),
    path('get_artist_user/', ArtistExtendedUpdateAPIView.as_view(), name='ArtistExtendedUpdateAPIView'),
    path('update_producer/', ProducerExtendedAPIView.as_view(), name='ProducerExtendedAPIView'),
    path('get_producer_user/', ProducerExtendedAPIView.as_view(), name='ProducerExtendedAPIView'),
    path('get_artists/', FilterApi.as_view(), name='FilterApi'),
    path('filter_artists/', FilterApi.as_view(), name='filter artists'),
    path('add_to_wishlist/', WishlistSaver.as_view(), name='wishlist'),
    path('get_related_wishlist/', WishlistSaver.as_view(), name='get related wishlist for a producer'),
    path('get_producer_request/', RequestContactApprover.as_view(), name='get_artist_related_wishlist'),
    path('approve_producer_request/', RequestContactApprover.as_view(), name='approve producer request'),
    path('dropdowns_for_artist/', artist_dropdowns, name='dropdowns_for_artist'),
    path('request_contact/', RequestContactSave.as_view(), name='request_contact'),
    path('view_requested_contacts/', RequestContactSave.as_view(), name='request_contact'),
    path('get_notifications/', get_notifications, name='get_notifications'),
]