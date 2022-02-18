from django.views.decorators.cache import cache_page
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework import status
from .models import DeclineOrganization, EcoSystem, Organization, Sector, SubEcosystem, SubecosystemSubclass
from .serializers import DeclineOrganizationSerializer, EcosystemSerializer, FileUploadSerializer, OrganizationSerializer, SectorSerializer, SubecosystemSerializer, SubecosystemSubclassSerializer
from account.permissions import IsAdminOrReadOnly, IsAdminUser_Custom
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import ValidationError, PermissionDenied
import cloudinary
import cloudinary.uploader
from drf_yasg.utils import swagger_auto_schema
from account.send_notice import User, send_notification
from .populate import process_data



SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS')


@swagger_auto_schema(methods=['POST'], request_body=OrganizationSerializer())
@api_view(['GET', 'POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticatedOrReadOnly])
def organizations(request):
    
    """Api view for adding and viewing all organizations. """

    if request.method == 'GET':
        organization = Organization.objects.filter(is_active=True, is_approved=True)

        serializer = OrganizationSerializer(organization, many =True)

        data = {
                'status'  : True,
                'message' : "Successful",
                'data' : serializer.data,
            }

        return Response(data, status=status.HTTP_200_OK)

    elif request.method == 'POST':

        serializer = OrganizationSerializer(data = request.data)

        if serializer.is_valid():
            try:
                if 'ceo_image' in serializer.validated_data.keys() and serializer.validated_data['ceo_image'] != None:
                    # upload the ceo's image
                    ceo_image = serializer.validated_data['ceo_image'] #get the image file from the request
                    img1 = cloudinary.uploader.upload(ceo_image, folder = 'edm/ceo_image/') #upload the image to cloudinary
                    serializer.validated_data['ceo_image'] = "" #delete the image file
                    
                    serializer.validated_data['ceo_image_url'] = img1['secure_url'] #save the image url
                else:
                    data = {
                    'status'  : False,
                    'message' : "Unsuccessful",
                    'error' : ["CEO's Image is required"],
                    }

                    return Response(data, status = status.HTTP_400_BAD_REQUEST)

                if 'company_logo' in serializer.validated_data.keys() and serializer.validated_data['company_logo'] != None:
                #upload the company's logo
                    company_logo = serializer.validated_data['company_logo'] #get the image file from the request
                    img2 = cloudinary.uploader.upload(company_logo, folder = 'edm/company_logo/') #upload the image to cloudinary
                    serializer.validated_data['company_logo'] = "" #delete the image file
                    serializer.validated_data['company_logo_url'] = img2['secure_url'] #save the image url



            except Exception as e:
                print(e)
                data = {
                    'status'  : False,
                    'message' : "Unsuccessful",
                    'error' : ["Unable to add organization"],
                }
                return Response(data, status = status.HTTP_400_BAD_REQUEST)

            organization = Organization.objects.create(**serializer.validated_data, user=request.user)
            
            send_notification(user=request.user, status='pending')

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


@swagger_auto_schema(methods=['PUT', 'DELETE'], request_body=OrganizationSerializer())
@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticatedOrReadOnly])
def organization_detail(request, pk):
    try:
        organization =  Organization.objects.get(pk = pk, is_active =True)

    except Organization.DoesNotExist:
        data = {
                'status'  : False,
                'error' : "Does not exist"
            }

        return Response(data, status=status.HTTP_404_NOT_FOUND)
    
    if request.method not in SAFE_METHODS and (organization.user != request.user or request.user.is_admin != True):
        raise PermissionDenied("You do not have the permission to perform this action")
    
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
            try:

                if 'ceo_image' in serializer.validated_data.keys() and serializer.validated_data['ceo_image'] != None:
                    ceo_image = serializer.validated_data['ceo_image'] #get the image file from the request
                    img2 = cloudinary.uploader.upload(ceo_image, folder = 'edm/ceo_image/') #upload the image to cloudinary
                    serializer.validated_data['ceo_image'] = "" #delete the image file
                    serializer.validated_data['ceo_image_url'] = img2['secure_url'] #save the image url

                if 'company_logo' in serializer.validated_data.keys() and serializer.validated_data['company_logo'] != None:
                    company_logo = serializer.validated_data['company_logo'] #get the image file from the request
                    img1 = cloudinary.uploader.upload(company_logo, folder = 'edm/company_logo/') #upload the image to cloudinary
                    serializer.validated_data['company_logo'] = "" #delete the image file
                    serializer.validated_data['company_logo_url'] = img1['secure_url'] #save the image url
            except Exception:
                data = {
                    'status'  : False,
                    'message' : "Unsuccessful",
                    'error' : ["Unable to update organization"],
                }
                return Response(data, status = status.HTTP_400_BAD_REQUEST)


            serializer.save()
            
            if request.user.is_admin:
                organization.is_approved=True
                organization.is_declined=False
                organization.responded=True
                organization.save()
            else:
                organization.is_approved=False
                organization.is_declined=False
                organization.responded=False
                organization.save()
                send_notification(request.user, status='updated')
                
            data = {
                'status'  : True,
                'message' : "Your request is pending approval.",
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

        organization.delete()

        data = {
                'status'  : True,
                'message' : "Deleted Successfully"
            }

        return Response(data, status = status.HTTP_204_NO_CONTENT)



@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAdminUser_Custom])
def pending_organizations(request):
    if request.method == 'GET':
        organization = Organization.objects.filter(is_active=True, responded =False)

        serializer = OrganizationSerializer(organization, many =True)

        data = {
                'status'  : True,
                'message' : "Successful",
                'data' : serializer.data,
            }

        return Response(data, status=status.HTTP_200_OK)


@swagger_auto_schema(methods=['POST'], request_body=EcosystemSerializer())
@api_view(['GET', 'POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAdminOrReadOnly])
def ecosystem(request):

    if request.method == 'GET':
        eco = EcoSystem.objects.filter(is_active=True)

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


@swagger_auto_schema(methods=['PUT', 'DELETE'], request_body=EcosystemSerializer())
@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAdminUser_Custom])
def ecosystem_detail(request, pk):
    try:
        eco =  EcoSystem.objects.get(pk = pk, is_active=True)

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


@swagger_auto_schema(methods=['POST'], request_body=SubecosystemSerializer())
@api_view(['GET', 'POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAdminOrReadOnly])
def sub_ecosystem(request):

    if request.method == 'GET':
        eco = SubEcosystem.objects.filter(is_active=True)

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


@swagger_auto_schema(methods=['PUT'], request_body=SubecosystemSerializer())
@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAdminUser_Custom])
def sub_ecosystem_detail(request, pk):
    try:
        eco =  SubEcosystem.objects.get(pk = pk, is_active=True)

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


@swagger_auto_schema(methods=['POST'], request_body=SectorSerializer())
@api_view(['GET', 'POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAdminOrReadOnly])
def sector(request):

    if request.method == 'GET':
        obj = Sector.objects.filter(is_active=True)

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

            serializer = SectorSerializer(obj)
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


@swagger_auto_schema(methods=['PUT'], request_body=SectorSerializer())
@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAdminUser_Custom])
def sector_detail(request, pk):
    try:
        obj =  Sector.objects.get(pk = pk, is_active=True)

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


@swagger_auto_schema(methods=['POST'], request_body=SubecosystemSubclassSerializer())
@api_view(['GET', 'POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAdminOrReadOnly])
def subclass(request):

    if request.method == 'GET':
        obj = SubecosystemSubclass.objects.filter(is_active=True)

        serializer = SubecosystemSubclassSerializer(obj, many =True)

        data = {
                'status'  : True,
                'message' : "Successful",
                'data' : serializer.data,
            }

        return Response(data, status=status.HTTP_200_OK)


    elif request.method == 'POST':

        serializer = SubecosystemSubclassSerializer(data = request.data)

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


@swagger_auto_schema(methods=['PUT'], request_body=SubecosystemSubclassSerializer())
@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAdminUser_Custom])
def subclass_detail(request, pk):
    try:
        obj =  SubecosystemSubclass.objects.get(pk = pk, is_active=True)

    except SubecosystemSubclass.DoesNotExist:
        data = {
                'status'  : False,
                'error' : "Does not exist"
            }

        return Response(data, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = SubecosystemSubclassSerializer(obj)

        data = {
                'status'  : True,
                'message' : "Successful",
                'data' : serializer.data,
            }

        return Response(data, status=status.HTTP_200_OK)

    #Update the item
    elif request.method == 'PUT':
        serializer = SubecosystemSubclassSerializer(obj, data = request.data, partial=True) #allows you to be able to update one field of the model

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
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticatedOrReadOnly])
def state(request):

    state = Organization.objects.values('state').distinct()


    filtered = {state[i]['state']: list(map(lambda x: x.org_dict(),Organization.objects.filter(state = state[i]['state']))) for i in range(len(state))}

    data = {
                'status'  : True,
                'message' : "Successful",
                'data' : filtered
            }

    return Response(data, status = status.HTTP_200_OK)

@swagger_auto_schema(methods=['POST'], request_body=FileUploadSerializer())
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAdminUser_Custom])
def upload_csv(request):

    if request.method == 'POST':

        serializer = FileUploadSerializer(data = request.data)


        if serializer.is_valid():

            file = serializer.validated_data['file']
            try:

                rows = process_data(file)
            except Exception:
                data = {
                'status'  : False,
                'message' : "Unsuccessful",
                'errors'  : ["Error uploading file.\n Please check that headers are correct."]

                }
                return Response(data, status = status.HTTP_400_BAD_REQUEST)

            # decoded_file = file.read().decode()

            # io_string = io.StringIO(decoded_file)

            # reader = csv.DictReader(io_string)
            success = False
            organizations = []
            for row in rows:
                success = False
                try:
                    if any(org.name == row['name'] for org in organizations) or Organization.objects.filter(name=row['name'], is_active=True).exists():
                        raise ValidationError(detail= {
                            'status'  : False,
                            'message' : "Unsuccessful",
                            'errors'  : [ f"Error uploading file.\nCannot upload multiple organizations or Organization '{row['name']}' already exists."]

                        })
                        
                    row['sector'] = Sector.objects.get(name = str(row['sector']))
                    row['ecosystem'] = EcoSystem.objects.get(name = str(row['ecosystem']))
                    row['sub_ecosystem'] = SubEcosystem.objects.get(name = str(row['sub_ecosystem']), ecosystem=row['ecosystem'])
                    
                    
                        
                    organizations.append(Organization(**row, is_active=True, is_approved=True, responded=True, user=request.user))

                    success = True
                except Exception:
                    success = False
            if success == True:
                Organization.objects.bulk_create(organizations)
                data = {
                    'status'  : True,
                    'message' : "File upload successful",

                }

                return Response(data, status = status.HTTP_200_OK)
            else:
                data = {
                'status'  : False,
                'message' : "Unsuccessful",
                'errors'  : ["Error uploading file.\n Please check that fields are correct."]

            }

            return Response(data, status = status.HTTP_400_BAD_REQUEST)

        else:
            data = {
                'status'  : False,
                'message' : "Unsuccessful",
                'errors'  : serializer.errors

            }

            return Response(data, status = status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAdminUser_Custom])
def approve_org(request, org_id):

    try:
        object = Organization.objects.get(id=org_id)

    except Organization.DoesNotExist:
        data = {
                'status'  : False,
                'error' : "Does not exist"
            }

        return Response(data, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':

        object.is_approved = True
        object.responded = True
        object.save()
        
        send_notification(user=object.user, status='approved')

        serializer = OrganizationSerializer(object)


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
                'error'   : 'Wrong HTTP Method. Required method is GET'
            }

        return Response(data, status = status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(methods=['POST'], request_body=DeclineOrganizationSerializer())
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAdminUser_Custom])
def reject_org(request, org_id):
    
    """ Make a post request with the reason why an organization is being declined. The "reason" key is the only value that should be passed."""
    user = request.user
        
    try:
        object = Organization.objects.get(id=org_id)

    except Organization.DoesNotExist:
        data = {
                'status'  : False,
                'error' : "Does not exist"
            }

        return Response(data, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'POST':
        serializer = DeclineOrganizationSerializer(data=request.data)

        if serializer.is_valid():
            DeclineOrganization.objects.create(**serializer.validated_data, organization=object, admin=user)
            
            
            object.is_declined = True
            object.responded = True
            object.save()
            send_notification(user=object.user, status='rejected', reason=serializer.validated_data['reason'])
            serializer = OrganizationSerializer(object)


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
                    'error'   : serializer.errors
                }

            return Response(data, status = status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAdminUser_Custom])
def rejected_org(request):
    
    if request.method == 'GET':
        organization = Organization.objects.all().filter(is_active=True, is_declined =True)

        serializer = OrganizationSerializer(organization, many =True)

        data = {
                'status'  : True,
                'message' : "Successful",
                'data' : serializer.data,
            }

        return Response(data, status=status.HTTP_200_OK)