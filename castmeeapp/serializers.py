from rest_framework import serializers
from .models import *


class ArtistExtendedSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArtistExtended
        exclude = [
            'languages_known','skills','consider_me_for','interest',
            'available_for','preferred_format','preferred_genre',
        ]

class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields=['name']


class SkillsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skills
        fields=['name']


class ConsiderMeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConsiderMe
        fields=['name']


class AvailableForSerializer(serializers.ModelSerializer):
    class Meta:
        model = AvailableFor
        fields=['name']


class PreferredFormatSerializer(serializers.ModelSerializer):
    class Meta:
        model = PreferredFormat
        fields=['name']


class PreferredGeneSerializer(serializers.ModelSerializer):
    class Meta:
        model = PreferredGene
        fields=['name']


class InterestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interest
        fields=['name']


class ArtistExtendedSerializerView(serializers.ModelSerializer):
    '''
    Customized serializer for artist view
    '''
    phone = serializers.SerializerMethodField('get_mobile_number')
    user_name =serializers.ReadOnlyField(source='artist.user.username')
    user_name =serializers.ReadOnlyField(source='artist.user.first_name')
    user_name =serializers.ReadOnlyField(source='artist.user.username')
    email =serializers.ReadOnlyField(source='artist.user.email')
    gender =serializers.ReadOnlyField(source='artist.gender')
    date_of_birth =serializers.ReadOnlyField(source='artist.date_of_birth')
    artist_id =serializers.ReadOnlyField(source='artist.id')
    hair_type =serializers.ReadOnlyField(source='hair_type.name')
    hair_color =serializers.ReadOnlyField(source='hair_color.name')
    body_type =serializers.ReadOnlyField(source='body_type.name')
    eye_color =serializers.ReadOnlyField(source='eye_color.name')
    skin_color =serializers.ReadOnlyField(source='eye_color.name')
    current_state =serializers.ReadOnlyField(source='eye_color.name')
    current_city =serializers.ReadOnlyField(source='eye_color.name')
    native_state =serializers.ReadOnlyField(source='eye_color.name')
    native_city =serializers.ReadOnlyField(source='eye_color.name')

    languages_known = LanguageSerializer(many=True, read_only=True)
    skills = SkillsSerializer(many=True, read_only=True)
    consider_me_for = ConsiderMeSerializer(many=True, read_only=True)
    available_for = AvailableForSerializer(many=True, read_only=True)
    preferred_format = PreferredFormatSerializer(many=True, read_only=True)
    preferred_genre = PreferredGeneSerializer(many=True, read_only=True)
    interest = InterestSerializer(many=True, read_only=True)


    def get_mobile_number(self,obj):
        artist_flg = self.context.get("artist",False)
        if artist_flg:
            return obj.artist.phone
        try:
            check_permission =WishList.objects.get(
                artist_id=obj.artist.id,
                producer_id = self.context.get('producer_id',None)
            )
        except WishList.DoesNotExist:
            return "Request for phone number"
        if check_permission.phone_view_status == 'pending':
            return "Waiting for approvel"
        elif  check_permission.phone_view_status=='approved' :
            return obj.artist.phone
        else :
            return ""
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


class WishListSerializer(serializers.ModelSerializer):
    '''
     serializer for wislist save
    '''
    class Meta:
        model = WishList
        fields = '__all__'


class ProducerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producer
        fields = '__all__'


class ProducerSerializerView(serializers.ModelSerializer):
    user_name = serializers.ReadOnlyField(source ='user.username')
    first_name = serializers.ReadOnlyField(source = 'user.first_name')
    last_name= serializers.ReadOnlyField(source = 'user.last_name')
    email = serializers.ReadOnlyField(source = 'user.email')

    class Meta:
        model = Producer
        fields = '__all__'


class ArtistSerializerView(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source= 'user.username')
    first_name = serializers.ReadOnlyField(source= 'user.first_name')
    last_name = serializers.ReadOnlyField(source= 'user.last_name')
    email = serializers.ReadOnlyField(source= 'user.email')
    class Meta:
        model = Artist
        fields= '__all__'
