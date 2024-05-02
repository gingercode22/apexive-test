# serializers.py

from rest_framework import serializers
from .models import Hotel, Room, Reservation


class HotelSerializer(serializers.ModelSerializer):
    total_days = serializers.SerializerMethodField()

    class Meta:
        model = Hotel
        fields = '__all__'

    def get_total_days(self, obj):
        return (obj.end - obj.start).days


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = '__all__'
