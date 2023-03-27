from django.db import models
from django.core.validators import MinLengthValidator, MaxLengthValidator

# Create your models here.

class EmployeeModel(models.Model):
    class AuthEmp(models.IntegerChoices):
        ADMIN = 1
        EMPLOYEE = 2
       
    emp_id = models.CharField(primary_key=True, null= False, max_length=4, 
                              validators=[MinLengthValidator(4), MaxLengthValidator(4)])
    emp_name = models.CharField(max_length=50, null= False)
    emp_password = models.CharField(max_length=16, validators=[MinLengthValidator(6)], null= False)
    emp_role = models.IntegerField(choices=AuthEmp.choices, default=AuthEmp.EMPLOYEE)