from .models import EmployeeModel
from rest_framework import serializers

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model  = EmployeeModel
        exclude = ['emp_password']