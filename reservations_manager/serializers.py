from .models import ReservationModel
from rest_framework import serializers

class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model  = ReservationModel
        exclude = []