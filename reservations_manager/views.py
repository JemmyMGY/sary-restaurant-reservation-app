from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework import viewsets
from rest_framework.response import Response
from .models import ReservationModel, TableModel
from .serializers import ReservationSerializer
from rest_framework import status
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError
from datetime import datetime
import copy
# Create your views here.

def get_free_slots(reserved_slots:list):
    if len(reserved_slots) > 0:
        datetime_now = datetime.now()
        working_time_end = datetime(datetime_now.year, datetime_now.month, datetime_now.day, 
                                                23, 59)
        free_slots = []
        curr_time = datetime_now
        reserved_slots_copy = copy.deepcopy(reserved_slots) 
        reserved_slots_copy.append((working_time_end, working_time_end))
        for slot in reserved_slots_copy:
            if slot[0] > curr_time:
                free_slots.append((curr_time, slot[0]))
            curr_time = slot[1]
        return free_slots
    return []

def get_table_reserved_slots(table_id):
    datetime_now = datetime.now()
    table_reserved_slots = ReservationModel.objects.filter(table_id = table_id).filter(start_time__gte=datetime_now).order_by('start_time').values_list('start_time', 'end_time')
    return list(table_reserved_slots)

def is_slot_found(table_reserved_slots:list, starting_time, ending_time):
    table_reserved_slots_copy = copy.deepcopy(table_reserved_slots)
    datetime_now = datetime.now()
    working_time_end = datetime(datetime_now.year, datetime_now.month, datetime_now.day, 
                                              23, 59)
    table_reserved_slots_copy.append((working_time_end, working_time_end))
    for counter in range(len(table_reserved_slots_copy)):
        if ending_time <= table_reserved_slots_copy[counter][0]:
            if counter == 0:
                return True
            else:
                if starting_time >= table_reserved_slots_copy[counter-1][1]:
                    return True
                else:
                    return False
    
    return False

class ReservationViewSet(viewsets.ModelViewSet):
    queryset = ReservationModel.objects.all()
    serializer_class = ReservationSerializer

    def destroy(self, request, *args, **kwargs):
        reservation_id = request.query_params['id']
        if ReservationModel.objects.filter(pk=reservation_id).count == 0:
            return Response(data="no reservation with id {0}".format(reservation_id), status=status.HTTP_204_NO_CONTENT)
        
        ReservationModel.objects.get(pk=reservation_id).delete()
        return Response(data="Successfully deleted reservation with id {0}".format(reservation_id), status=status.HTTP_200_OK)

    def list(self, request, *args, **kwargs):
        if len(self.queryset) == 0:
            return Response(data="No reservations found!!")
        
        return Response(data=self.serializer_class(self.queryset, many=True).data, status=status.HTTP_200_OK)
    
    def create(self, request, *args, **kwargs):
        datetime_now = datetime.now()
        working_time_start = datetime(datetime_now.year, datetime_now.month, datetime_now.day, 
                                              12, 00)
        working_time_end = datetime(datetime_now.year, datetime_now.month, datetime_now.day, 
                                              23, 59)
        
        start_time_str = (request.query_params['start_time']).split(":")
        end_time_str = (request.query_params['end_time']).split(":")
        table_id = request.query_params['table_id']
        # print(start_time_str, end_time_str)
        if len(TableModel.objects.filter(pk=table_id)) == 0:
            return Response(data="FAILED, No registered table found with id = {0}".format(table_id), status=status.HTTP_406_NOT_ACCEPTABLE)
        
        starting_time =  datetime(datetime_now.year, datetime_now.month, datetime_now.day, 
                                             int(start_time_str[0]), int(start_time_str[1]))
        ending_time =  datetime(datetime_now.year, datetime_now.month, datetime_now.day, 
                                             int(end_time_str[0]), int(end_time_str[1]))
        print(start_time_str, end_time_str)
        if starting_time < working_time_start:
            return Response(data="FAILED, starting time is out of working hours", status=status.HTTP_406_NOT_ACCEPTABLE)
        
        if ending_time > working_time_end:
            return Response(data="FAILED, starting time is out of working hours", status=status.HTTP_406_NOT_ACCEPTABLE)
        
        if ending_time <= starting_time:
            return Response(data="FAILED, ending time should be greater than starting time", status=status.HTTP_406_NOT_ACCEPTABLE)
        
        if starting_time < datetime_now :
             return Response(data="FAILED, starting time should be after or equal to current time", status=status.HTTP_406_NOT_ACCEPTABLE)
        
        table_reserved_slots = get_table_reserved_slots(table_id)
        
        if is_slot_found(table_reserved_slots, starting_time, ending_time):
            
            try:
                add_reservation = ReservationModel.objects.create(start_time=starting_time, end_time = ending_time, 
                                    table_id = TableModel.objects.get(pk=table_id) , reservation_id = "{0}||{1}||{2}".format(str(starting_time), str(ending_time), table_id))
                add_reservation.clean()
                
            except:
                error_msg = "Caught Exception"
                return Response(data=error_msg, status=status.HTTP_406_NOT_ACCEPTABLE)

            add_reservation.save()
            return Response(data="Added reservation for table with id = {0}, start_time = {1}, end_time = {2}".format(table_id, str(starting_time), str(ending_time)), status=status.HTTP_200_OK)
        else:
            return Response(data="FAILED, Couldn't find free slot between {0} and {1} for the table with id = {2}".format(str(starting_time), str(ending_time), table_id), status=status.HTTP_406_NOT_ACCEPTABLE)
        
    def get_todays_reservations(self, request, *args, **kwargs):
        datetime_now = datetime.now()
        query_set = ReservationModel.objects.filter(start_time__date = datetime(datetime_now.year,datetime_now.month,datetime_now.day))
        return  Response(data=self.serializer_class(query_set, many=True).data, status=status.HTTP_200_OK)

    def get_available_slots(self, request, *args, **kwargs):
        num_seats=request.query_params['seats']

        tables_based_seats = list(TableModel.objects.filter(table_seats = num_seats).values_list('table_id', flat=True))
        table_to_reserved_slots = {}
        for table_id in tables_based_seats:
            table_reserved_slots = get_table_reserved_slots(table_id)
            table_free_slots = get_free_slots(table_reserved_slots)
            table_to_reserved_slots[table_id] = table_free_slots
        
        return Response(data=table_to_reserved_slots, status=status.HTTP_200_OK)
