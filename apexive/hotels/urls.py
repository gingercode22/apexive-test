# urls.py

from django.urls import path
from .views import HotelListCreateAPIView, RoomListCreateAPIView, reservation_list

urlpatterns = [
    path('hotels/', HotelListCreateAPIView.as_view(), name='hotel-list-create'),
    path('hotels/<int:hotel_id>/rooms/', RoomListCreateAPIView.as_view(), name='room-list-create'),
    path('rooms/<int:room_id>/reservations/', reservation_list, name='reservation-list'),
]
