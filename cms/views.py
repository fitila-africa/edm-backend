from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from . models import AboutUsContent
from . serializers import AboutUsContentSerializer
# Create your views here.

@api_view(['GET', 'PUT'])
def aboutus(request, id):
    try:
        aboutus = AboutUsContent.objects.get(id=id)
    except AboutUsContent.DoesNotExist:
        return Response({'message':'Does not exist'}, status=status.HTTP_404_NOT_FOUND)
        
    if request.method == 'GET':
        serializer = AboutUsContentSerializer(aboutus)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    if request.method == 'PUT':
        serializer = AboutUsContentSerializer(aboutus, data=request.data)
        if serializer.is_valid():
            serializer.save()
            
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)