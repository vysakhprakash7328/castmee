from rest_framework import serializers
from .models import *


class Talent_user_registration_serializer(serializers.ModelSerializer):
    class Meta:
        model = Talant_user_details
        fields = '__all__'


class Get_talent_user_details_serializer(serializers.ModelSerializer):
    
    class Meta:
        model = Talant_user_details
        fields = '__all__'


