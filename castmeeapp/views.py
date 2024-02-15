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


def generate_random_password(length=12):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(secrets.choice(characters) for _ in range(length))
    return password

class Talent_user_registration_API(APIView):
    def post(self, request):
        data = request.data

        random_password = generate_random_password()
        print("Random Password:", random_password)

        user = User(
            first_name=data['name'],
            email=data['email'],
        )

        user.set_password(random_password)

        user.save()

        user_details = User.objects.get(email=data['email'])


        data['user_id'] = user_details.id

        serializer = Talent_user_registration_serializer(data=data)

        if serializer.is_valid():
            serializer.save()

            return Response({
                "message": "Registration successful",
                "success": True,
                "password": random_password,
            }, status=status.HTTP_201_CREATED)

        return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
       

class TalentLogin_API(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user)

            return Response({
                'user_id':user.id,
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
        serializer_recruiter = Talent_recruiter_registration_seriailizer(data=data.get('recruiter_details'))
        serializer_recruiter_freelancer = Talent_recruiter_registration_seriailizer(data=data.get('recruiter_freelancer_details'))
        serializer_company_recruiter = Talent_recruiter_registration_seriailizer(data=data.get('recruiter_company_details'))

        if (
            serializer_recruiter.is_valid() and
            serializer_recruiter_freelancer.is_valid() and
            serializer_company_recruiter.is_valid()
        ):
            serializer_recruiter.save()
            serializer_company_recruiter.save()
            serializer_recruiter_freelancer.save()
            return Response({"message": "registration successful"}, status=status.HTTP_201_CREATED)

        return Response(status=status.HTTP_400_BAD_REQUEST)
    

class Find_a_talent_API(APIView):
    def get(self, request):
        data = request.data
        model_class = apps.get_model('castmeeapp',data['model'])
    

    



            




