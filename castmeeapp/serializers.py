from rest_framework import serializers
from .models import *


class ArtistExtendedSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArtistExtended
        exclude = [
            'languages_known','skills','consider_me_for','interest',
            'available_for','preferred_format','preferred_genre',
        ]


class ArtistExtendedSerializerView(serializers.ModelSerializer):
    '''
    Customized serializer for artist view
    '''
    class Meta:
        model = ArtistExtended
        fields = '__all__'


class ProducerExtendedSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProducerExtended
        fields = '__all__'


class ProducerExtendedSerializerView(serializers.ModelSerializer):
    '''
    Customized serializer for producer view
    '''
    class Meta:
        model = ProducerExtended
        fields = '__all__'
