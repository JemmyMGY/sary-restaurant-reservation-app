from django.db import models
from tables_manager.models import TableModel
# Create your models here.
class ReservationModel(models.Model):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    table_id = models.ForeignKey(TableModel, on_delete=models.CASCADE)
    reservation_id = models.CharField(primary_key=True, max_length=255)