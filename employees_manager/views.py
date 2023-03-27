from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework import viewsets
from rest_framework.response import Response
from .models import EmployeeModel
from .serializers import EmployeeSerializer
from rest_framework import status
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = EmployeeModel.objects.all()
    serializer_class = EmployeeSerializer

    def destroy(self, request, *args, **kwargs):
        emp_id = request.query_params['id']
        
        if len(EmployeeModel.objects.filter(pk=emp_id)) == 0:
             return Response(data="Can't find employee with given id", status=status.HTTP_404_NOT_FOUND)
        
        EmployeeModel.objects.get(emp_id=emp_id).delete()
        return Response(data="Employee with id = {0} has been deleted!".format(emp_id), status=status.HTTP_200_OK)
    
    def list(self, request, *args, **kwargs):
        if EmployeeModel.objects.count() < 1:
            return Response(data="There are no Employess yet", status=status.HTTP_204_NO_CONTENT)
        return Response(data = self.serializer_class(self.queryset, many=True).data, status=status.HTTP_202_ACCEPTED)
    
    def create(self, request, *args, **kwargs):
        employee_info = request.query_params
        emp_id = employee_info['id']
        emp_name=employee_info['name']
        emp_password=employee_info['password']
        emp_role = employee_info['role']

        if not emp_id or not emp_name or not emp_password or not emp_role:
            return Response(data="Failed to save employee due to Invalid input data" ,status=status.HTTP_406_NOT_ACCEPTABLE)
        
        if len(employee_info['id']) != 4:
                error_msg = "employee id should consist of 4 digits"
                return Response(data=error_msg, status=status.HTTP_406_NOT_ACCEPTABLE)
        if len(employee_info['password']) < 6:
                error_msg = "employee password should consist of 6 characters at least"
                return Response(data=error_msg, status=status.HTTP_406_NOT_ACCEPTABLE)
           
        try:
            add_emp = EmployeeModel.objects.create(emp_id=emp_id, 
                          emp_name=emp_name, 
                          emp_password=emp_password, 
                          emp_role = emp_role)   
            add_emp.full_clean()

        except IntegrityError:
            error_msg = "Integrity Error"
            
            if EmployeeModel.objects.get(emp_id=employee_info['id']):
                error_msg = "there is another employee with this id before"
                
            return Response(data=error_msg ,status=status.HTTP_406_NOT_ACCEPTABLE)
        
        except ValidationError:
            error_msg = "Validation Error"
            
            if len(employee_info['id']) != 4:
                error_msg = "employee id should consist of 4 digits"
            elif len(employee_info['password']) < 6:
                error_msg = "employee password should consist of 6 characters at least"
           
            return Response(data=error_msg, status=status.HTTP_406_NOT_ACCEPTABLE)
        except:
            return Response(data= "FAILED, didn't save", status=status.HTTP_406_NOT_ACCEPTABLE)
        
        add_emp.save()
        success_msg = "successfully saved employee with id = {0} and name = {1}".format(emp_id, emp_name)
        return Response(data=success_msg, status=status.HTTP_201_CREATED)
        