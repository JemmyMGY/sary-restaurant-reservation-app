from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework import viewsets
from rest_framework.response import Response
from .models import TableModel
from reservations_manager.models import ReservationModel
from .serializers import TableSerializer
from rest_framework import status
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError




from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken

class JWTAuthenticationSafe(JWTAuthentication):
    def authenticate(self, request):
        try:
            return super().authenticate(request=request)
        except InvalidToken:
            return None

class TablesViewSet(viewsets.ModelViewSet):
    queryset = TableModel.objects.all()
    serializer_class = TableSerializer
    # permission_classes = IsAuthenticated
    
    def destroy(self, request, *args, **kwargs):
        table_id = request.query_params['id']
        
        if len(TableModel.objects.filter(table_id=table_id)) == 0:
            return Response(data="Can't find table with given id", status=status.HTTP_404_NOT_FOUND)
        
        table = TableModel.objects.get(table_id=table_id)
        if len(ReservationModel.objects.filter(table_id=table_id)) > 0:
            return Response(data="Can't delete table with id = {0}, it has reservations!!".format(table_id), status= status.HTTP_409_CONFLICT) 
        else:
            table.delete()
            return Response(data="table with id = {0} has been deleted!".format(table_id), status=status.HTTP_200_OK)

    def list(self, request, *args, **kwargs):
        if len(self.queryset) < 1:
            return Response(data="There are no Tables yet", status=status.HTTP_200_OK)
        return Response(data=self.serializer_class(self.queryset, many=True).data, status=status.HTTP_200_OK)
     
    def create(self, request, *args, **kwargs):
        table_id = request.query_params['id']
        table_seats = request.query_params['seats']

        if not table_id or not table_seats:
            return Response(data="Invalid data, table id and table seats shouldn't be empty/None", status=status.HTTP_400_BAD_REQUEST)
        
        
        table_id = int(table_id)
        table_seats = int(table_seats)
        try:
            add_table = TableModel.objects.create(table_id=table_id, table_seats=table_seats)
            add_table.full_clean()
        except IntegrityError:
            error_msg = "Integrity Error"
            table = TableModel.objects.filter(table_id=table_id)
            if len(table) > 0:
                error_msg = "There is another table with the same id"
            return Response(data=error_msg, status=status.HTTP_406_NOT_ACCEPTABLE)
        except ValidationError:
            error_msg = "Validation Error" 
            if table_seats > 12  or table_seats < 1:
                error_msg = "{0} is invalid value, it should be between [1, 12]".format(table_seats)
                
            return Response(data=error_msg, status=status.HTTP_406_NOT_ACCEPTABLE)
        except:
            return Response(data= "didn't save", status=status.HTTP_503_SERVICE_UNAVAILABLE)
        
        try:    
            add_table.save()
        except:
            return Response(data = "Error happened while saving table", status= status.HTTP_500_INTERNAL_SERVER_ERROR)
        success_msg = "successfully saved table with id = {0} and seats {1}".format(table_id, table_seats)
        return Response(data=success_msg, status=201)
       