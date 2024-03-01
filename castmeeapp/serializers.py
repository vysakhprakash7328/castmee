from rest_framework import serializers
from .models import *


class Talent_user_registration_serializer(serializers.ModelSerializer):
    class Meta:
        model = Talent_user_details
        fields = '__all__'


class Get_talent_user_details_serializer(serializers.ModelSerializer):
    '''
    Talent user serializer with all data
    '''
    name = serializers.ReadOnlyField(source = 'user_id.first_name')
    user_id= serializers.ReadOnlyField(source = 'user_id.id')
    username = serializers.ReadOnlyField(source='user_id.username')
    email = serializers.ReadOnlyField(source='user_id.email')

    
    class Meta:
        model = Talent_user_details
        fields = '__all__'

class Talent_recruiter_registration_seriailizer(serializers.ModelSerializer):
    '''
    Talent recruiter details with all data
    '''
    name =  serializers.ReadOnlyField(source = 'recruiter_id.first_name')
    user_id = serializers.ReadOnlyField(source = 'recruiter_id.id')
    username = serializers.ReadOnlyField(source = 'recruiter_id.username')
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

class Talent_user_language_serializer(serializers.ModelSerializer):
    class Meta:
        model = Talent_user_languages
        fields = '__all__'
class Talent_user_skills_serializer(serializers.ModelSerializer):
    class Meta:
        model = Talent_user_skills
        fields = '__all__'




