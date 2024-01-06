from rest_framework import serializers
from .models import *


class Talent_user_registration_serializer(serializers.ModelSerializer):
    class Meta:
        model = Talent_user_details
        fields = '__all__'


class Get_talent_user_details_serializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField(source = 'user_id.firstname')
    
    class Meta:
        model = Talent_user_details
        fields = '__all__'

class Talent_recruiter_registration_seriailizer(serializers.ModelSerializer):
    class Meta:
        model = Talent_recruiter_details
        fields = '__all__'

class Talent_recruiter_freelancer_details_serializer(serializers.ModelSerializer):
    class Meta:
        model = freelance_recruiter_details
        fields = '__all__'

class Talent_recruiter_company_details_serializer(serializers.ModelSerializer):
    class Meta:
        model = company_recruiter_details
        fields = '__all__'




