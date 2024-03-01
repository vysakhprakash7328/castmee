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
from rest_framework.decorators import api_view


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
        ''''
        Method for login both talent user and recruiter
        '''
        username = request.data.get('username')
        password = request.data.get('password')
        type_of_user = request.data.get("type")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            access_token =str(refresh.access_token)
            data ={
                 "access_token":access_token,
                 "refresh_token":str(refresh)
                }
            if type_of_user == 'talent_user':
                try:
                    talent_user_data =Talent_user_details.objects.get(user_id = user)

                except Talent_user_details.DoesNotExist:
                    return Response({
                        "detail":"Are your sure a Talent user ? Please check",
                        "success":False
                    },status=status.HTTP_406_NOT_ACCEPTABLE
                    )
                data['user_data']= Get_talent_user_details_serializer(talent_user_data).data

            else :
                try :
                    talent_recruiter_data = Talent_recruiter_details.objects.get(recruiter_id = user)

                except Talent_recruiter_details.DoesNotExist:
                    return Response({
                        "detail":"Are your sure a Recruiter ? Please check",
                        "success":False
                    },status=status.HTTP_406_NOT_ACCEPTABLE
                    )
                data['user_data'] = Talent_recruiter_registration_seriailizer(talent_recruiter_data).data
                
            return Response({
                "detail":data,"success":True
            },status=status.HTTP_200_OK
            )

        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        


class Get_talent_user_details_API(APIView):
    def get(self, request):
        queryset = Talent_user_details.objects.filter(request.data['user_id'])
        serializer = Get_talent_user_details_serializer(queryset, many=True)
        return Response({"data":serializer.data}, status= status.HTTP_200_OK) 


class RegistrationAPI(APIView):
    def post(self, request):
        '''
        Api for registering both recruiter and talent
        '''
        data = request.data
        user_type = data.pop('type',None)
        if user_type is None:
            return Response({
                "detail":"Please give user type",
                "success":False
            },status=status.HTTP_406_NOT_ACCEPTABLE)

        username = data["username"]
        if User.objects.filter(username=username).exists():
            return Response({
                "detail":"Username already taken ,please choose different one",
                "success":False
            },status=status.HTTP_406_NOT_ACCEPTABLE
            )
        email = data['email']
        if User.objects.filter(email=email).exists():
            return Response({
                "detail":"Already registered email,exisisting user ?",
                "success":False
            },status=status.HTTP_406_NOT_ACCEPTABLE
            )
        
        password=data.pop('password',None)
        if password is None:
            return Response({
                "detail":"Please provide password",
                "success":False
            },status=status.HTTP_406_NOT_ACCEPTABLE
            )
        confirm_password = data.pop('confirm_password',None)
        if password != confirm_password:
            return Response({
                "detail":"Password miss match",
                "success":False
            },status=status.HTTP_406_NOT_ACCEPTABLE
            )

        user= User.objects.create(
            username = username,
            email = email,
            first_name = data.pop('first_name')
        )
        user.set_password(password)
        user.save()

        if user_type == 'talent_user':
            Talent_user_details.objects.create(
                user_id = user,
                age =  data.get('age',None),
                address = data.get('address',None),
                gender = data.get('gender',None),

            )
        else :
            Talent_recruiter_details.objects.create(
                recruiter_id = user,
                recruiter_phone = data.get('recruiter_phone'),
                freelancer_or_company = data.get('freelancer_or_company')
            )
        
        return Response({
            "detail":"Successfully Registered,Please verify your profile ","success":True
        },status=status.HTTP_201_CREATED
        )


@api_view(["GET"])
def get_dropdowns(request):
    '''
    api for giving all master dropdowns
    '''
    data={
    "skill_master_dropdown" : {obj.id:obj.skill for obj in Skills_master.objects.all()},
    "language_master_dropdown" : {obj.id:obj.language for obj in Language_master.objects.all()},
    "project_type_dropdown":{obj.id:obj.project_type for obj in Project_type_master.objects.all()}
    }
    return Response({
        "detail":data,
        "success":True
    },status=status.HTTP_200_OK
    )
    

class UpdationAPI(APIView):
    '''
    Api for updating data of both recruiter & freelancer according to usertype
    '''
    def post(self,request):
        data = request.data
        user_type = data.pop("type",None)
        if user_type is None:
            return Response({
                "detail":"Please give user type",
                "success":False
            },status=status.HTTP_406_NOT_ACCEPTABLE)
        
        user_id = data.pop('user_id',None)
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({
                "detail":"User not found,please register",
                "success":False
            },status=status.HTTP_406_NOT_ACCEPTABLE
            )
        if user_type == 'talent_user':
            language = data.pop("language",[])
            language = [Language_master.objects.get(id = x) for x in language]
            skills = data.pop("skills",[])
            skills = [Skills_master.objects.get(id = x) for x in skills]

            talent_user = Talent_user_details.objects.get(user_id =user)
            language_instance,created = Talent_user_languages.objects.get_or_create(talent_user=talent_user)
            language_instance.language.add(*language)
            skill_instance,created = Talent_user_skills.objects.get_or_create(talent_user=talent_user)
            skill_instance.skills.add(*skills)

            seria = Talent_user_registration_serializer(
                talent_user,
                data = data,
                partial = True
            )
            if seria.is_valid():
                seria.save()
                return Response({
                    "detail":"Successfully Updated data",
                    "success":True
                },status=status.HTTP_200_OK
                )
            else:
                return Response({
                    "detail":seria.errors,"success":False
                },status=status.HTTP_400_BAD_REQUEST
                )
        else :
            recruiter = Talent_recruiter_details.objects.get(recruiter_id= user)
            if "recruiter_phone" in data.keys():
                recruiter.recruiter_phone = data.pop('recruiter_phone')
            if 'freelancer_or_company' in data.keys():
                recruiter.freelancer_or_company = data.pop('freelancer_or_company')

            recruiter.save()
            data["talent_recruiter_id"]=recruiter.id
            freelancer_or_company = recruiter.freelancer_or_company
            current_serializer = Talent_recruiter_freelancer_details_serializer
            if freelancer_or_company=='company':
                current_serializer = Talent_recruiter_company_details_serializer
            
            seria = current_serializer(data=data)
            if seria.is_valid():
                seria.save()
                return Response({
                    "detail":"Successfully Updated data",
                    "success":True
                },status=status.HTTP_200_OK
                )
            else:
                return Response({
                    "detail":seria.errors,"success":False
                },status=status.HTTP_400_BAD_REQUEST
                )


class FilterAPI(APIView):
    def post(self,request):
        condition = request.data
        if 'username' in condition.keys():
            condition["user_id__username"]= condition.pop("username")
        if 'first_name' in condition.keys():
            condition['user_id__first_name']=condition.pop('first_name')
        if "email" in condition.keys():
            condition['user_id__email']=condition.pop('email')

        data = Talent_user_details.objects.filter(**condition)
        seria = Get_talent_user_details_serializer(data,many=True)
        return Response({
            "detail":seria.data,'success':True
        },status=status.HTTP_200_OK
        )

    def get(self,request):
        '''
        get a single talent full data based user id
        '''
        user_id = request.query_params.get('user_id')
        try:
            user = User.objects.get(id = user_id)
        except User.DoesNotExist:
            return Response({
                "detail":"User not found",
                "success":False
            },status=status.HTTP_404_NOT_FOUND
            )
        talent_user = Talent_user_details.objects.get(user_id=user)
        seria = Get_talent_user_details_serializer(talent_user)
        return Response({
            "detail":seria.data,'success':True
        },status=status.HTTP_200_OK
        )





