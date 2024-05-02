from datetime import date
from django.db.models.expressions import OuterRef, Exists, Subquery
from django.db.models.functions import Coalesce
from django.db.models import Count
from django.db import models
from django.utils import timezone



class RoomQuerySet(models.QuerySet):
    def get_rooms_list_with_sold_out_sign(self, move_in: date, move_out: date):
        from apexive.hotels.models import Reservation

        return self.annotate(
            sold_out=Exists(
                Reservation.objects
                .filter(
                    models.Q(start__range=(move_in, move_out)) | models.Q(
                        end__range=(move_in, move_out)),
                    room_id=OuterRef('id'),
                )
            )
        )


class HotelQuerySet(models.QuerySet):
    def get_with_only_one_room(self):
        from apexive.hotels.models import Room, Reservation
        now = timezone.now()

        free_rooms_count_subquery = Subquery(
            Room.objects
            .annotate(
                is_occupied=(Exists(
                    Reservation.objects.filter(
                        start__lte=now,
                        end__gte=now,
                        room_id=OuterRef('pk'),
                    )
                )
                ))
            .filter(
                is_occupied=False,
                hotel_id=OuterRef('id'),
            )
            .values('hotel_id')
            .annotate(cnt=Count("id"))
            .values("cnt")
        )

        hotels = self.annotate(
            free_rooms_count=Coalesce(free_rooms_count_subquery, 0)
        ).filter(free_rooms_count=1)
        return hotels
