from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, MinLengthValidator, MaxLengthValidator

# Create your models here.
class TableModel(models.Model):
    table_id = models.IntegerField(primary_key=True)
    table_seats = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(12)])


