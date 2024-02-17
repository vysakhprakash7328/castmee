import secrets
import string
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import *
from django.apps import apps
from django.db import IntegrityError 

def generate_random_password(length=12):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(secrets.choice(characters) for _ in range(length))
    return password

class Talent_user_registration_API(APIView):
    def post(self, request):
        data = request.data

        random_password = generate_random_password()
        print("Random Password:", random_password)
        if User.objects.filter(email = data['email']):
            return Response("Email already exist",status=status.HTTP_303_SEE_OTHER)
        else:
        
            try:
                user = User(
                    first_name=data['name'],
                    email=data['email'],
                    username=data['username']
                )
                user.set_password(random_password)
                user.save()
            except IntegrityError:
                return Response("The username '{}' is already taken. Please choose a different username.".format(data['username']))
        
            user_details = User.objects.get(username=data['username'])
        


            data['user_id'] = user_details.id

            serializer = Talent_user_registration_serializer(data=data)

            if serializer.is_valid():
                serializer.save()
                talent_user_id = Talent_user_details.objects.get(user_id = user_details.id).id
                lang_list = []
                skill_list = []
                for lang in data['language']:
                    languages = {}
                    languages['talent_user'] = talent_user_id
                    languages['language'] = lang
                    lang_list.append(languages)

                for skill in data['skills']:
                    skills = {}
                    skills['talent_user'] = talent_user_id
                    skills['skills'] = skill
                    skill_list.append(skills)

                print(skill_list)
                print(lang_list)
                
                for data in skill_list:
                    talent_user_instance = Talent_user_details.objects.get(pk=data['talent_user'])
                    
                    skills_names = data['skills']
                    skills_instances = []
                    skill_instance= Skills_master.objects.get(skill=skills_names)
                    skills_instances.append(skill_instance)
                
                    talent_user_skills_instance = Talent_user_skills.objects.create(talent_user=talent_user_instance)
                    talent_user_skills_instance.skills.set(skills_instances)
                for data in lang_list:
                    talent_user_instance = Talent_user_details.objects.get(pk=data['talent_user'])
                    
                    lang_names = data['language']
                    print(lang_names)
                    lang_instances = []
                    lang_instance= Language_master.objects.get(language=lang_names)
                    lang_instances.append(lang_instance)
                    
                    talent_user_lang_instance = Talent_user_languages.objects.create(talent_user=talent_user_instance)
                    talent_user_lang_instance.language.set(lang_instances)
                return Response({
                    "message": "Registration successful",
                    "success": True,
                    "password": random_password,
                }, status=status.HTTP_201_CREATED)

            return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        

class Login_API(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user)

            if Talent_user_details.objects.filter(user_id = User.objects.get(id = user.id)):
                type = 'talent_user'
            else:
                type = 'talent_recruiter'

            return Response({
                'user_id':user.id,
                'username':User.objects.get(id = user.id).username,
                'name':User.objects.get(id = user.id).first_name,
                'type':type,
                'access_token': str(refresh.access_token),
                'refresh_token': str(refresh),
            }, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        


class Get_talent_user_details_API(APIView):
    def get(self, request):
        queryset = Talent_user_details.objects.filter(request.data['user_id'])
        serializer = Get_talent_user_details_serializer(queryset, many=True)
        return Response({"data":serializer.data}, status= status.HTTP_200_OK) 
    

class TalentRecruiterRegistrationAPI(APIView):
    def post(self, request):
        data = request.data
        first_name=data['recruiter_details'].pop('recruiter_name'),
        email=data['recruiter_details'].pop('recruiter_email'),
        username = data['recruiter_details'].pop('recruiter_username')
        try:
            user = User(
                first_name=first_name,
                email=email,
                username=username
            )
            password = data['recruiter_details'].pop('recruiter_password')
            user.set_password(password)
            user.save()
        except IntegrityError:
            return Response("The username '{}' is already taken. Please choose a different username.".format(username))
        user_details = User.objects.get(username=username)
        data['recruiter_details']['recruiter_id'] = user_details.id

        serializer_recruiter = Talent_recruiter_registration_seriailizer(data=data.get('recruiter_details'))
        if serializer_recruiter.is_valid():
            serializer_recruiter.save()
            talent_recruiter_id = Talent_recruiter_details.objects.get(recruiter_id_id = user_details.id).id
            if 'freelancer_details' in data:
                data['freelancer_details']['talent_recruiter_id']= talent_recruiter_id
                serializer_recruiter_freelancer = Talent_recruiter_freelancer_details_serializer(data=data.get('freelancer_details'))
                if serializer_recruiter_freelancer.is_valid():
                    serializer_recruiter_freelancer.save()
                else:
                    serializer_recruiter_freelancer.errors()
            elif 'company_details' in data:
                data['company_details']['talent_recruiter_id']= talent_recruiter_id
                serializer_recruiter_company = Talent_recruiter_company_details_serializer(data=data.get('company_details'))
                if serializer_recruiter_company.is_valid():
                    serializer_recruiter_company.save()
                else:
                    serializer_recruiter_company.errors()


            return Response({"message": "registration successful"}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer_recruiter.errors())
        




    



            




