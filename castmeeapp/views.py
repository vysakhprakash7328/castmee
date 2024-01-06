import secrets
import string
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import Talent_user_registration_serializer
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

def generate_random_password(length=12):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(secrets.choice(characters) for _ in range(length))
    return password

class Talent_user_registration_api(APIView):
    def post(self, request):
        data = request.data
        user = User()
        random_password = generate_random_password()
        print("Random Password:", random_password)

        user.first_name = data['name']
        user.email = data['email']
        user.set_password(random_password)

        data.pop('name')
        data.pop('email')

        serializer = Talent_user_registration_serializer(data=data)
        if serializer.is_valid():
            user.save()
            serializer.save()
            return Response({"message": "Registration successful", "success": True}, status=status.HTTP_201_CREATED)
        return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        request.data['user_id']
    

class TalentUserLogin(APIView):
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
        




            




