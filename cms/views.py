from account.permissions import IsAdminOrReadOnly, IsAdminUser_Custom
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from . models import *
from . serializers import *
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework_simplejwt.authentication import JWTAuthentication
from drf_yasg.utils import swagger_auto_schema
# Create your views here.

# @api_view(['GET', 'PUT'])
# def aboutus(request, id):
#     try:
#         aboutus = AboutUsContent.objects.get(id=id)
#     except AboutUsContent.DoesNotExist:
#         return Response({'message':'Does not exist'}, status=status.HTTP_404_NOT_FOUND)
        
#     if request.method == 'GET':
#         serializer = AboutUsContentSerializer(aboutus)
        
#         return Response(serializer.data, status=status.HTTP_200_OK)
    
#     if request.method == 'PUT':
#         serializer = AboutUsContentSerializer(aboutus, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
            
#             return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(method='post', request_body=FAQSerializer())
@api_view(['GET', 'POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAdminOrReadOnly])
def faq(request):
    
    """ Enables only admin users to create new frequently asked questions while others can only view. """
    if request.method == 'GET':
        obj = FAQ.objects.filter(is_active=True)
        serializer = FAQSerializer(obj, many=True)
        
        data = {
                'status'  : True,
                'message' : "Successful",
                'data' : serializer.data,
            }

        return Response(data, status = status.HTTP_200_OK)
        

    if request.method == 'POST':
        
        serializer = FAQSerializer(data = request.data)

        if serializer.is_valid():

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


@swagger_auto_schema(method='put', request_body=FAQSerializer())
@api_view(['GET', 'PUT', 'DELETE']) 
@authentication_classes([JWTAuthentication])
@permission_classes([IsAdminUser_Custom])
def faq_detail(request, faq_id):
    """ Allows only admin users to edit and delete frequently asked questions. """
    try:
        obj =  FAQ.objects.get(id = faq_id, is_active =True)
    
    except FAQ.DoesNotExist:
        data = {
                'status'  : False,
                'error' : "Does not exist"
            }

        return Response(data, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = FAQSerializer(obj)
        
        data = {
                'status'  : True,
                'message' : "Successful",
                'data' : serializer.data,
            }

        return Response(data, status=status.HTTP_200_OK)

    #Update the item
    elif request.method == 'PUT':
        serializer = FAQSerializer(obj, data = request.data, partial=True) #allows you to be able to update one field of the model

        if serializer.is_valid():

            serializer.save()

            data = {
                'status'  : True,
                'message' : "Successful",
                'data' : serializer.data,
            }

            return Response(data, status = status.HTTP_202_ACCEPTED)

        else:
            data = {
                'status'  : False,
                'message' : "Unsuccessful",
                'error' : serializer.errors,
            }

            return Response(data, status = status.HTTP_400_BAD_REQUEST)

    #de-activate the item
    elif request.method == 'DELETE':
        
        obj.delete()
        
        data = {
                'status'  : True,
                'message' : "Deleted Successfully"
            }

        return Response(data, status = status.HTTP_204_NO_CONTENT)
