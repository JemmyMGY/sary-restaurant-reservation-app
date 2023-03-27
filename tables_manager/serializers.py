from .models import TableModel
from rest_framework import serializers

class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model  = TableModel
        exclude =[]
