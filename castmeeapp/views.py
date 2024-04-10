
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
import json
from .models import *
from django.apps import apps
from django.db import IntegrityError 
from rest_framework.decorators import api_view
import ast


class ArtistCreateAPIView(APIView):
    def post(self, request, format=None):
        payload = request.data
        if User.objects.filter(username=payload['username']).exists():
            return Response({
                "detail":"username already taken","success":False
            },status=status.HTTP_406_NOT_ACCEPTABLE
        )
        if User.objects.filter(email=payload['email']).exists() :
            return Response({
                "detail":"email already registered","success":False
            },status=status.HTTP_406_NOT_ACCEPTABLE
        )
        password = payload.get("password")
        confirm_password = payload.get("confirm_password")
        if password != confirm_password:
            return Response({
                "detail":"Password mismatch","success":False
            },status=status.HTTP_406_NOT_ACCEPTABLE
        )
        user_data = {
            'username': payload.get('username'),
            'email': payload.get('email'),
            'first_name': payload.get('first_name'),
            'last_name': payload.get('last_name')
        }
        artist_data = {
            'phone': payload.get('phone'),
            'gender': payload.get('gender'),
            # 'looking_for_work': payload.get('looking_for_work'),
            'date_of_birth': payload.get('date_of_birth'),
        }
        user = User.objects.create(**user_data) 
        user.set_password(password)
        user.save()
        artist_data['user'] = user  # Set the user for the artist
        artist = Artist.objects.create(**artist_data)
        ArtistExtended.objects.create(artist=artist)

        return Response({
            "detail":"Account created successfully","success":True
        },status=status.HTTP_201_CREATED
        )


class ProducerCreateAPIView(APIView):
    def post(self, request, format=None):
        payload = request.data
        if User.objects.filter(username=payload['username']).exists():
            return Response({
                "detail":"username already taken","success":False
            },status=status.HTTP_406_NOT_ACCEPTABLE
        )
        if User.objects.filter(email=payload['email']).exists() :
            return Response({
                "detail":"email already registered","success":False
            },status=status.HTTP_406_NOT_ACCEPTABLE
        )
        password = payload.get("password")
        confirm_password = payload.get("confirm_password")
        if password != confirm_password:
            return Response({
                "detail":"Password mismatch","success":False
            },status=status.HTTP_406_NOT_ACCEPTABLE
        )
        user_data = {
            'username': payload.get('username'),
            'email': payload.get('email'),
            'first_name': payload.get('first_name'),
            'last_name': payload.get('last_name')
        }
        user = User.objects.create(**user_data)
        user.set_password(password)
        user.save()
        payload['user']=user.id  # Set the user for the producer
        producer = ProducerSerializer(data = payload)
        if producer.is_valid():
            producer.save()
            return Response({
                'detail': 'Producer created successfully',"success":True
            }, status=status.HTTP_201_CREATED
            )
        else:
            return Response({
                'detail': producer.errors,"success":False
            }, status=status.HTTP_400_BAD_REQUEST
            )


class Login(APIView):
    def post(self, request, format=None):
        username = request.data.get('username')
        password = request.data.get('password')
        user_type = request.data.get('user_type',None)
        if user_type is None:
            return Response({
                "detail":"provide user type","success":False
            },status=status.HTTP_400_BAD_REQUEST)
        user = authenticate(username=username, password=password)
        refresh = RefreshToken.for_user(user)
        access = refresh.access_token
        if user is not None:
            if user_type == 'producer':
                try :
                    producer = Producer.objects.get(user = user)
                except Producer.DoesNotExist:
                    return Response({
                        "detail":"user is not an producer","success":False
                    },status=status.HTTP_406_NOT_ACCEPTABLE
                )
                if producer.admin_approved == False:
                    return Response({
                        "detail":"Please wait untill admin approves","success":False
                    },status=status.HTTP_400_BAD_REQUEST
                )
                response_data = ProducerSerializerView(producer).data
                response_data ={
                    "user_type":"producer",
                    "data":response_data,
                    "refresh": str(refresh),
                    "access": str(access),
                }
                return Response({
                    "data":response_data,"success":True
                    }, status=status.HTTP_200_OK
                )
            elif user_type == 'artist':
                try: 
                    artist = Artist.objects.get(user=user)
                except Artist.DoesNotExist:
                    return Response({
                        "detail":"user is not an artist","success":False
                    },status=status.HTTP_406_NOT_ACCEPTABLE
                    )
                response_data = ArtistSerializerView(artist).data
                response_data ={
                    "user_type":"artist",
                    "data":response_data,
                    "refresh": str(refresh),
                    "access": str(access),
                }
                return Response({
                    "data":response_data,"success":True
                    }, status=status.HTTP_200_OK
                )
            else:
                 return Response({
                'detail': 'Invalid user type',"success":False
            }, status=status.HTTP_400_BAD_REQUEST
        )

        else:
            return Response({
                'detail': 'Invalid credentials',"success":False
            }, status=status.HTTP_401_UNAUTHORIZED
        )


class MasterDropdowns(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        user_type = request.query_params.get("user_type",None)
        if user_type is not None:
            if user_type == 'producer':
                response_data ={}
                return Response({
                    "detail":response_data,"success":True
                },status=status.HTTP_200_OK
                )
            elif user_type == 'artist':
                response_data ={
                    'hair_type':[{obj.id:obj.name} for obj in HairType.objects.all()],
                    'hair_color':[{obj.id:obj.name} for obj in HairColor.objects.all()],
                    'body_type':[{obj.id:obj.name} for obj in BodyType.objects.all()],
                    'eye_color':[{obj.id:obj.name} for obj in EyeColor.objects.all()],
                    'skin_color':[{obj.id:obj.name} for obj in SkinColor.objects.all()],
                    'state':[{obj.id:obj.name} for obj in State.objects.all()],
                    'city':[{obj.id:obj.name} for obj in City.objects.all()],
                    'language':[{obj.id:obj.name} for obj in Language.objects.all()],
                    'skills':[{obj.id:obj.name} for obj in Skills.objects.all()],
                    'consider_me_for':[{obj.id:obj.name} for obj in ConsiderMe.objects.all()],
                    'available_for':[{obj.id:obj.name} for obj in AvailableFor.objects.all()],
                    'preferred_format':[{obj.id:obj.name} for obj in PreferredFormat.objects.all()],
                    'preferred_genre':[{obj.id:obj.name} for obj in PreferredGene.objects.all()],
                    'interest':[{obj.id:obj.name} for obj in Interest.objects.all()],
                }
                return Response({
                    "detail":response_data,"success":True
                },status=status.HTTP_200_OK
                )
            else:
                return Response({
                    "detail":f"{user_type} is not supported",'success':False
                },status=status.HTTP_400_BAD_REQUEST
                )
        else:
            return Response({
                'detail': 'provide user type',"success":False
            }, status=status.HTTP_401_UNAUTHORIZED
        )


class ArtistExtendedUpdateAPIView(APIView):
    '''
    Class for getting and updating artist extended data
    '''
    permission_classes = [IsAuthenticated]
    def get_object(self, artist_id):
        try:
            return ArtistExtended.objects.get(artist_id=artist_id)
        except ArtistExtended.DoesNotExist:
            return None

    def put(self, request):
        artist_id = request.data.get("artist_id",None)
        if artist_id is None:
            return Response({
                "detail":"provide artist id","success":False
            },status=status.HTTP_406_NOT_ACCEPTABLE)
        artist_extended = self.get_object(artist_id)
        if artist_extended is None:
            return Response({
                "detail":"Artist not Found","success":False
            },status=status.HTTP_404_NOT_FOUND)

        if  'multipart/form-data' in request.content_type:
            languages_known = request.data.get('languages_known',None)
            if languages_known is not None:
                languages_= json.loads(languages_known)
                language_instances = Language.objects.filter(id__in=languages_)
                artist_extended.languages_known.add(*language_instances)

            skills = request.data.get('skills',None)
            if skills is not None:
                skills= json.loads(skills)
                skill_instances= Skills.objects.filter(id__in=skills)
                artist_extended.skills.add(*skill_instances)

            consider_me_for = request.data.get('consider_me_for',None)
            if consider_me_for is not None:
                consider_me_for= json.loads(consider_me_for)
                consider_me_for_instances= ConsiderMe.objects.filter(id__in=consider_me_for)
                artist_extended.consider_me_for.add(*consider_me_for_instances)

            available_for = request.data.get("available_for",None)
            if available_for is not None:
                available_for= json.loads(available_for)
                available_for_instances= AvailableFor.objects.filter(id__in=available_for)
                artist_extended.available_for.add(*available_for_instances)

            preferred_format = request.data.get("preferred_format",None)
            if preferred_format is not None:
                preferred_format= json.loads(preferred_format)
                preferred_format_instances= PreferredFormat.objects.filter(id__in=preferred_format)
                artist_extended.preferred_format.add(*preferred_format_instances)

            preferred_genre = request.data.get('preferred_genre',None)
            if preferred_genre is not None:
                preferred_genre= json.loads(preferred_genre)
                preferred_genre_instances= PreferredGene.objects.filter(id__in=preferred_genre)
                artist_extended.preferred_genre.add(*preferred_genre_instances)

            interest = request.data.get("interest",None)
            if interest is not None:
                interest= json.loads(interest)
                interest_= Interest.objects.filter(id__in=interest)
                artist_extended.interest.add(*interest_)

        serializer = ArtistExtendedSerializer(artist_extended, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            data = ArtistExtendedSerializerView(artist_extended,context={"artist":True}).data
            return Response({
                "detail":data,"success":True
            },status=status.HTTP_200_OK)
        return Response({
            "detail":serializer.errors,"success":False
        }, status=status.HTTP_400_BAD_REQUEST)

    def get(self,request):
        user_id = request.user.id
        try:
            user = User.objects.get(id = user_id)
        except User.DoesNotExist:
            return Response({
                "detail":"user not found","sucess":False
            },status=status.HTTP_400_BAD_REQUEST
        )
        try:
            artist = Artist.objects.get(user_id = user.id)
        except Artist.DoesNotExist:
           return Response({
                "detail":"Are you really an artist","sucess":False
            },status=status.HTTP_400_BAD_REQUEST
        )
        artist_extended = ArtistExtended.objects.get(artist_id = artist.id)
        serialized_data = ArtistExtendedSerializerView(artist_extended).data
        return Response({
            "detail":serialized_data,"success":True
            },status=status.HTTP_200_OK
        )


class ProducerExtendedAPIView(APIView):
    '''
    class for get and update a single producer data
    '''

    permission_classes = [IsAuthenticated]
    def get_object(self, producer_id):
        try:
            return ProducerExtended.objects.get(producer_id=producer_id)
        except ProducerExtended.DoesNotExist:
            return None

    def put(self, request):
        producer_id = request.data.get("producer_id",None)
        if producer_id is None:
            return Response({
                "detail":"provide producer id","success":False
            },status=status.HTTP_406_NOT_ACCEPTABLE)
        producer_extended = self.get_object(producer_id)
        if producer_extended is None:
            return Response({
                "detail":"producer not Found","success":False
            },status=status.HTTP_404_NOT_FOUND)

        serializer = ProducerExtendedSerializer(producer_extended, data=request.data,partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "detail":serializer.data,"success":True
            },status=status.HTTP_200_OK)
        return Response({
            "detail":serializer.errors,"success":False
        }, status=status.HTTP_400_BAD_REQUEST)


    def get(self,request):
        user_id = request.user.id
        try:
            user = User.objects.get(id = user_id)
        except User.DoesNotExist:
            return Response({
                "detail":"user not found","sucess":False
            },status=status.HTTP_400_BAD_REQUEST
        )
        try:
            producer = Producer.objects.get(user_id = user.id)
        except Producer.DoesNotExist:
           return Response({
                "detail":"Are you really an producer","sucess":False
            },status=status.HTTP_400_BAD_REQUEST
        )
        producer_extended = ProducerExtended.objects.get(producer_id = producer.id)
        serialized_data = ProducerExtendedSerializerView(producer_extended).data
        return Response({
            "detail":serialized_data,"success":True
            },status=status.HTTP_200_OK
        )


class FilterApi(APIView):
    permission_classes=[IsAuthenticated]
    def get(self, request):
        artists = ArtistExtended.objects.all()
        serializer = ArtistExtendedSerializerView(artists, many=True)
        return Response({
            "detail":serializer.data,"success":True
        }, status=status.HTTP_200_OK
    )
    def post(self,request):
        filters = request.data
        artists = ArtistExtended.objects.filter(**filters)
        serializer = ArtistExtendedSerializerView(artists, many=True)
        return Response({
            "detail":serializer.data,"success":True
        }, status=status.HTTP_200_OK
    )


class WishlistSaver(APIView):
    '''
    
    '''
    def post(self,request):
        '''
        Api for adding wishlist
        '''
        try:
            producer = Producer.objects.get(id= request.data.get('producer_id',None))
        except Producer.DoesNotExist:
            return Response({
                "detail":"no producer found","success":False
            },status=status.HTTP_400_BAD_REQUEST)
        try:
            artist = Artist.objects.get(id=request.data.get("artist_id",None))
        except  Artist.DoesNotExist:
            return Response({
                "detail":"no artist found","success":False
            },status=status.HTTP_400_BAD_REQUEST)
        
        validate_data = WishListSerializer(data=request.data)
        if validate_data.is_valid():
            validate_data.save()
            return Response({
                "detail":"Successfully added to wish list","success":True
            },status=status.HTTP_200_OK)
        else:
            return Response({
                "detail":"Something went wrong","success":False
            },status=status.HTTP_400_BAD_REQUEST)
