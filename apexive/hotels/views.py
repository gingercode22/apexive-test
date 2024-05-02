# views.py
from django.shortcuts import get_object_or_404


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, action
from .models import Hotel, Room, Reservation
from .serializers import HotelSerializer, RoomSerializer, ReservationSerializer


class HotelListCreateAPIView(APIView):
    def get(self, request):
        hotels = Hotel.objects.all()
        serializer = HotelSerializer(hotels, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = HotelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(['POST'], detail=True)
    def like(self, request, pk):
        hotel = get_object_or_404(Hotel, pk=pk)
        hotel.likes += 1
        hotel.save(update_fields=['likes'])
        return Response({'status': 'likes increased'})

    @action(['POST'], detail=True)
    def dislike(self, request, pk):
        hotel = get_object_or_404(Hotel, pk=pk)
        hotel.dislikes -= 1
        hotel.save(update_fields=['dislikes'])
        return Response({'status': 'dislikes increased'})


    @action(['GET'], detail=False)
    def hotels_with_only_one_free_room(self, request):
        hotels = Hotel.objects.get_with_only_one_room()
        serializer = HotelSerializer(hotels, many=True)
        return Response(serializer.data)


class RoomListCreateAPIView(APIView):
    def get(self, request, hotel_id):
        rooms = Room.objects.filter(hotel_id=hotel_id)
        serializer = RoomSerializer(rooms, many=True)
        return Response(serializer.data)

    def post(self, request, hotel_id):
        request.data['hotel'] = hotel_id
        serializer = RoomSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def reservation_list(request, room_id):
    reservations = Reservation.objects.filter(room_id=room_id)
    serializer = ReservationSerializer(reservations, many=True)
    return Response(serializer.data)
