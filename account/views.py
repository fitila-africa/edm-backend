from drf_yasg import openapi
from rest_framework.decorators import api_view, authentication_classes, permission_classes 
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .serializers import UserSerializer
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth import authenticate

from django.contrib.auth.signals import user_logged_in

import cloudinary
import cloudinary.uploader
from drf_yasg.utils import swagger_auto_schema


@swagger_auto_schema(methods=['POST'], request_body=UserSerializer())
@api_view(['POST'])
# @authentication_classes([JWTAuthentication])
# @permission_classes([IsAuthenticated])
def add_user(request):

    if request.method == 'POST':
        
        serializer = UserSerializer(data = request.data)
        
        if serializer.is_valid():

            #upload profile picture
            # profile_pics = serializer.validated_data['profile_pics'] #get the image file from the request 
            # img1 = cloudinary.uploader.upload(profile_pics, folder = 'fitila/profile pictures/') #upload the image to cloudinary
            # serializer.validated_data['profile_pics'] = "" #delete the image file
            # serializer.validated_data['profile_pics_url'] = img1['secure_url'] #save the image url 
            
            #hash password
            serializer.validated_data['password'] = make_password(serializer.validated_data['password']) #hash the given password
            user = User.objects.create(**serializer.validated_data)
            

            serializer = UserSerializer(user)
            data = {
                'status'  : True,
                'message' : "Successful",
                'data' : serializer.data,
            }

            return Response(data, status = status.HTTP_201_CREATED)

        else:
            data = {
                'status'  : False,
                'message' : "Unsuccessful",
                'error' : serializer.errors,
            }

            return Response(data, status = status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(methods=['POST'], request_body=UserSerializer())
@api_view(['POST'])
# @authentication_classes([JWTAuthentication])
# @permission_classes([IsAuthenticated])
def add_admin(request):

    if request.method == 'POST':
        
        serializer = UserSerializer(data = request.data)
        
        if serializer.is_valid():

            
            
            #hash password
            serializer.validated_data['password'] = make_password(serializer.validated_data['password']) #hash the given password
            user = User.objects.create(**serializer.validated_data, is_admin=True, is_staff=True)
            

            serializer = UserSerializer(user)
            data = {
                'status'  : True,
                'message' : "Successful",
                'data' : serializer.data,
            }

            return Response(data, status = status.HTTP_201_CREATED)

        else:
            data = {
                'status'  : False,
                'message' : "Unsuccessful",
                'error' : serializer.errors,
            }

            return Response(data, status = status.HTTP_400_BAD_REQUEST)





@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_user(request):
    if request.method == 'GET':
        user = User.objects.filter(is_active=True)
    
        
        serializer = UserSerializer(user, many =True)
        data = {
                'status'  : True,
                'message' : "Successful",
                'data' : serializer.data,
            }

        return Response(data, status=status.HTTP_200_OK)


#Get the detail of a single user by their ID

@swagger_auto_schema(methods=['PUT', 'DELETE'], request_body=UserSerializer())
@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def user_detail(request):
    try:
        user = User.objects.get(id = request.user.id, is_active=True)
    
    except User.DoesNotExist:
        data = {
                'status'  : False,
                'message' : "Does not exist"
            }

        return Response(data, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = UserSerializer(user)
        
        data = {
                'status'  : True,
                'message' : "Successful",
                'data' : serializer.data,
            }

        return Response(data, status=status.HTTP_200_OK)

    #Update the profile of the user
    elif request.method == 'PUT':
        serializer = UserSerializer(user, data = request.data, partial=True) #allows you to be able to update one field of the model

        if serializer.is_valid():
            
            #check if it's password change and hash the new password
            if "password" in serializer.validated_data.keys():
                serializer.validated_data['password'] = make_password(serializer.validated_data['password'])
        
            serializer.save()

            data = {
                'status'  : True,
                'message' : "Successful",
                'data' : serializer.data,
            }

            return Response(data, status = status.HTTP_201_CREATED)

        else:
            data = {
                'status'  : False,
                'message' : "Unsuccessful",
                'error' : serializer.errors,
            }

            return Response(data, status = status.HTTP_400_BAD_REQUEST)

    #delete the account
    elif request.method == 'DELETE':
        user.is_active = False
        user.save()

        data = {
                'status'  : True,
                'message' : "Deleted Successfully"
            }

        return Response(data, status = status.HTTP_204_NO_CONTENT)



@swagger_auto_schema(method='post', request_body=openapi.Schema(
    type=openapi.TYPE_OBJECT, 
    properties={
        'email': openapi.Schema(type=openapi.TYPE_STRING, description='string'),
        'password': openapi.Schema(type=openapi.TYPE_STRING, description='string'),
    }
))
@api_view([ 'POST'])
def user_login(request):
    
    if request.method == "POST":
        
        user = authenticate(request, email = request.data['email'], password = request.data['password'])
        if user is not None and user.is_active==True:
            try:
                
                refresh = RefreshToken.for_user(user)

                user_detail = {}
                user_detail['id']   = user.id
                user_detail['first_name'] = user.first_name
                user_detail['last_name'] = user.last_name
                user_detail['email'] = user.email
                user_detail['role'] = user.role
                user_detail['is_admin'] = user.is_admin
                user_detail['refresh'] = str(refresh)
                user_detail['access'] = str(refresh.access_token)
                user_logged_in.send(sender=user.__class__,
                                    request=request, user=user)

                data = {
                'status'  : True,
                'message' : "Successful",
                'data' : user_detail,
                }
                return Response(data, status=status.HTTP_200_OK)


            except Exception as e:
                raise e

        else:
            data = {
                'status'  : False,
                'error': 'Please provide a valid email and a password'
                }
            return Response(data, status=status.HTTP_401_UNAUTHORIZED)