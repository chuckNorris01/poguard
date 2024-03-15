from django.db import IntegrityError

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated

from .customheader import CustomHeaderAuthentication
from .models import POGaurd
from .serializers import POGaurdSerializer
from .filters import POGaurdFilter



class POGaurdView(APIView):
    authentication_classes = [SessionAuthentication, CustomHeaderAuthentication]
    permission_classes = [IsAuthenticated]
    filter_class = POGaurdFilter
    
    def get(self, request, *args, **kwargs) -> Response:        
        queryset = POGaurdFilter(request.query_params, queryset=POGaurd.objects.all()).qs
        ordering_fields:list[str] = request.query_params.getlist('ordering', [])

        if ordering_fields:
            queryset = queryset.order_by(*ordering_fields)
        serializer = POGaurdSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def post(self, request) -> Response:
        serializer = POGaurdSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if IntegrityError:
            return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class POGaurdViewDetail(APIView):
    authentication_classes = [SessionAuthentication, CustomHeaderAuthentication]
    permission_classes = [IsAuthenticated]
    
    # internal po ID not Brightpearl po ID
    def get_poGaurd_instance(self, identifier:int) -> int|None:
        try:
            return POGaurd.objects.get(pk=identifier) 
        except POGaurd.DoesNotExist:
            try:
                return POGaurd.objects.get(poNumber=identifier)
            except POGaurd.DoesNotExist:
                return None
        
    def get(self, request, identifier:int) -> Response:
        po_number:int|None = self.get_poGaurd_instance(identifier)
        if po_number:
            serializer = POGaurdSerializer(po_number)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'detail': 'PO Number not found'}, status=status.HTTP_404_NOT_FOUND)
    
    def patch(self, request, identifier:int) -> Response:
        po_number:int|None = self.get_poGaurd_instance(identifier)
        if po_number:
            serializer = POGaurdSerializer(po_number, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'detail': 'PO Number not found'}, status=status.HTTP_404_NOT_FOUND)
    
    def delete(self, request, identifier:int) -> Response:
        po_number:int|None = self.get_poGaurd_instance(identifier)
        if po_number:
            po_number.delete()
            return Response({"detail": "PO Number deleted"}, status=status.HTTP_204_NO_CONTENT)
        return Response({"detail": "PO Number not found"}, status=status.HTTP_404_NOT_FOUND)
