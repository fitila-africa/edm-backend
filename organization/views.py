from django.shortcuts import render
from rest_framework.decorators import api_view, authentication_classes, permission_classes 
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import EcoSystem, Organization, Sector, SubEcosystem
from .serializers import EcosystemSerializer, FileUploadSerializer, OrganizationSerializer, SectorSerializer, SubecosystemSerializer
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
import cloudinary
import cloudinary.uploader
import csv
import io

# Create your views here.


@api_view(['GET'])
# @authentication_classes([JSONWebTokenAuthentication])
# @permission_classes([IsAuthenticated])
def organizations(request):
    
    if request.method == 'GET':
        organization = Organization.objects.all().filter(is_active=True)
    
        serializer = OrganizationSerializer(organization, many =True)

        data = {
                'status'  : True,
                'message' : "Successful",
                'data' : serializer.data,
            }

        return Response(data, status=status.HTTP_200_OK)


@api_view(['POST'])
# @authentication_classes([JSONWebTokenAuthentication])
# @permission_classes([IsAuthenticated])
def add_organization(request):

    if request.method == 'POST':
        
        serializer = OrganizationSerializer(data = request.data)

        if serializer.is_valid():

            if serializer.validated_data['company_logo'] is not None:
            #upload the company's logo
                company_logo = serializer.validated_data['company_logo'] #get the image file from the request 
                img1 = cloudinary.uploader.upload(company_logo, folder = 'fitila/company_logo/') #upload the image to cloudinary
                serializer.validated_data['company_logo'] = "" #delete the image file
                serializer.validated_data['company_logo_url'] = img1['secure_url'] #save the image url 
            else: 
                data = {
                'status'  : False,
                'message' : "Unsuccessful",
                'error' : ["Company logo is required"],
            }

                return Response(data, status = status.HTTP_400_BAD_REQUEST)

            if serializer.validated_data['ceo_image'] is not None:
            # upload the ceo's image
                ceo_image = serializer.validated_data['ceo_image'] #get the image file from the request 
                img2 = cloudinary.uploader.upload(ceo_image, folder = 'fitila/ceo_image/') #upload the image to cloudinary
                serializer.validated_data['ceo_image'] = "" #delete the image file
                serializer.validated_data['ceo_image_url'] = img2['secure_url'] #save the image url 
            else: 
                data = {
                'status'  : False,
                'message' : "Unsuccessful",
                'error' : ["CEO's Image is required"],
            }

                return Response(data, status = status.HTTP_400_BAD_REQUEST)

            
            organization = Organization.objects.create(**serializer.validated_data)
            organization.save()

            serializer = OrganizationSerializer(organization)
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



@api_view(['GET', 'PUT', 'DELETE']) 
# @authentication_classes([JSONWebTokenAuthentication])
# @permission_classes([IsAuthenticated])
def organization_detail(request, pk):
    try:
        organization =  Organization.objects.get(pk = pk, is_active =True)
    
    except Organization.DoesNotExist:
        data = {
                'status'  : False,
                'error' : "Does not exist"
            }

        return Response(data, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = OrganizationSerializer(organization)
        
        data = {
                'status'  : True,
                'message' : "Successful",
                'data' : serializer.data,
            }

        return Response(data, status=status.HTTP_200_OK)

    #Update the item
    elif request.method == 'PUT':
        serializer = OrganizationSerializer(organization, data = request.data, partial=True) #allows you to be able to update one field of the model

        if serializer.is_valid():

            if 'ceo_image' in serializer.validated_data.keys():
                ceo_image = serializer.validated_data['ceo_image'] #get the image file from the request 
                img2 = cloudinary.uploader.upload(ceo_image, folder = 'fitila/ceo_image/') #upload the image to cloudinary
                serializer.validated_data['ceo_image'] = "" #delete the image file
                serializer.validated_data['ceo_image_url'] = img2['secure_url'] #save the image url

            if 'company_logo' in serializer.validated_data.keys():
                company_logo = serializer.validated_data['company_logo'] #get the image file from the request 
                img1 = cloudinary.uploader.upload(company_logo, folder = 'fitila/company_logo/') #upload the image to cloudinary
                serializer.validated_data['company_logo'] = "" #delete the image file
                serializer.validated_data['company_logo_url'] = img1['secure_url'] #save the image url 


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

    #de-activate the item
    elif request.method == 'DELETE':
        
        organization.is_active = False
        organization.save() 
        
        data = {
                'status'  : True,
                'message' : "Deleted Successfully"
            }

        return Response(data, status = status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
# @authentication_classes([JSONWebTokenAuthentication])
# @permission_classes([IsAuthenticated])
def ecosystem(request):
    
    if request.method == 'GET':
        eco = EcoSystem.objects.all()
    
        serializer = EcosystemSerializer(eco, many =True)

        data = {
                'status'  : True,
                'message' : "Successful",
                'data' : serializer.data,
            }

        return Response(data, status=status.HTTP_200_OK)


    elif request.method == 'POST':
        
        serializer = EcosystemSerializer(data = request.data)
        
        if serializer.is_valid():
        
            eco = EcoSystem.objects.create(**serializer.validated_data)
            eco.save()

            serializer = EcosystemSerializer(eco)
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



@api_view(['GET', 'PUT', 'DELETE']) 
# @authentication_classes([JSONWebTokenAuthentication])
# @permission_classes([IsAuthenticated])
def ecosystem_detail(request, pk):
    try:
        eco =  EcoSystem.objects.get(pk = pk)
    
    except EcoSystem.DoesNotExist:
        data = {
                'status'  : False,
                'error' : "Does not exist"
            }

        return Response(data, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = EcosystemSerializer(eco)
        
        data = {
                'status'  : True,
                'message' : "Successful",
                'data' : serializer.data,
            }

        return Response(data, status=status.HTTP_200_OK)

    #Update the item
    elif request.method == 'PUT':
        serializer = EcosystemSerializer(eco, data = request.data, partial=True) #allows you to be able to update one field of the model

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

    #de-activate the item
    elif request.method == 'DELETE':
        
        eco.delete()
        
        data = {
                'status'  : True,
                'message' : "Deleted Successfully"
            }

        return Response(data, status = status.HTTP_204_NO_CONTENT)       


@api_view(['GET', 'POST'])
# @authentication_classes([JSONWebTokenAuthentication])
# @permission_classes([IsAuthenticated])
def sub_ecosystem(request):
    
    if request.method == 'GET':
        eco = SubEcosystem.objects.all()
    
        serializer = SubecosystemSerializer(eco, many =True)

        data = {
                'status'  : True,
                'message' : "Successful",
                'data' : serializer.data,
            }

        return Response(data, status=status.HTTP_200_OK)


    elif request.method == 'POST':
        
        serializer = SubecosystemSerializer(data = request.data)
        
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



@api_view(['GET', 'PUT', 'DELETE']) 
# @authentication_classes([JSONWebTokenAuthentication])
# @permission_classes([IsAuthenticated])
def sub_ecosystem_detail(request, pk):
    try:
        eco =  SubEcosystem.objects.get(pk = pk)
    
    except SubEcosystem.DoesNotExist:
        data = {
                'status'  : False,
                'error' : "Does not exist"
            }

        return Response(data, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = SubecosystemSerializer(eco)
        
        data = {
                'status'  : True,
                'message' : "Successful",
                'data' : serializer.data,
            }

        return Response(data, status=status.HTTP_200_OK)

    #Update the item
    elif request.method == 'PUT':
        serializer = SubecosystemSerializer(eco, data = request.data, partial=True) #allows you to be able to update one field of the model

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

    #de-activate the item
    elif request.method == 'DELETE':
        
        eco.delete()
        
        data = {
                'status'  : True,
                'message' : "Deleted Successfully"
            }

        return Response(data, status = status.HTTP_204_NO_CONTENT) 

@api_view(['GET', 'POST'])
# @authentication_classes([JSONWebTokenAuthentication])
# @permission_classes([IsAuthenticated])
def sector(request):
    
    if request.method == 'GET':
        obj = Sector.objects.all()
    
        serializer = SectorSerializer(obj, many =True)

        data = {
                'status'  : True,
                'message' : "Successful",
                'data' : serializer.data,
            }

        return Response(data, status=status.HTTP_200_OK)


    elif request.method == 'POST':
        
        serializer = SectorSerializer(data = request.data)
        
        if serializer.is_valid():
        
            obj = Sector.objects.create(**serializer.validated_data)
            obj.save()

            serializer = EcosystemSerializer(obj)
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



@api_view(['GET', 'PUT', 'DELETE']) 
# @authentication_classes([JSONWebTokenAuthentication])
# @permission_classes([IsAuthenticated])
def sector_detail(request, pk):
    try:
        obj =  Sector.objects.get(pk = pk)
    
    except Sector.DoesNotExist:
        data = {
                'status'  : False,
                'error' : "Does not exist"
            }

        return Response(data, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = SectorSerializer(obj)
        
        data = {
                'status'  : True,
                'message' : "Successful",
                'data' : serializer.data,
            }

        return Response(data, status=status.HTTP_200_OK)

    #Update the item
    elif request.method == 'PUT':
        serializer = SectorSerializer(obj, data = request.data, partial=True) #allows you to be able to update one field of the model

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

    #de-activate the item
    elif request.method == 'DELETE':
        
        obj.delete()
        
        data = {
                'status'  : True,
                'message' : "Deleted Successfully"
            }

        return Response(data, status = status.HTTP_204_NO_CONTENT)  


@api_view(['GET'])
def state(request):

    state = Organization.objects.values('state').distinct()


    print([state[i]['state'] for i in range(len(state))])
    filtered = {state[i]['state']: list(map(lambda x: {"id":x.id,
                                                "name":x.name, 
                                                "company_logo_url": x.company_logo_url, "ceo_image_url":x.ceo_image_url, "state":x.state, 
                                                "sector":x.sector,
                                                "employee" :x.num_of_employees, "funding":x.funding
                                                },Organization.objects.filter(state = state[i]['state']))) for i in range(len(state))}

    data = {
                'status'  : True,
                'message' : "Successful",
                'data' : filtered
            }

    return Response(data, status = status.HTTP_200_OK)


@api_view(['POST'])
def upload_csv(request):

    
    if request.method == 'POST':
        
        serializer = FileUploadSerializer(data = request.data)
        

        if serializer.is_valid():
            
            file = serializer.validated_data['file']
            
            decoded_file = file.read().decode()
            
            io_string = io.StringIO(decoded_file)
            
            reader = csv.DictReader(io_string)
            
            for row in reader:
                print(row)
                row['ecosystem'] = EcoSystem.objects.get(name = str(row['ecosystem']))
                row['sub_ecosystem'] = SubEcosystem.objects.get(name = str(row['sub_ecosystem']), ecosystem=row['ecosystem'])
                
                Organization.objects.create(**row, is_active=True )

            
            
            data = {
                'status'  : True,
                'message' : "File upload successful",
                
            }

            return Response(data, status = status.HTTP_200_OK)

        else:
            data = {
                'status'  : False,
                'message' : "Unsuccessful",
                'errors'  : serializer.errors
                
            }

            return Response(data, status = status.HTTP_400_BAD_REQUEST)


        